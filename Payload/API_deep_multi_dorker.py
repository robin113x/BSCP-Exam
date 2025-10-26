#!/usr/bin/env python3
"""
deep_multi_dorker.py

Passive OSINT dork generator + multi-engine URL builder + optional Google Custom Search API integration + regex filtering + markdown report export.

Usage examples:
    # generate dorks and print URLs
    python3 deep_multi_dorker.py example.com --out report.md

    # open queries in browser for manual review (safe, manual inspection)
    python3 deep_multi_dorker.py example.com --open

    # use Google Custom Search API to fetch results (requires API_KEY and CX)
    python3 deep_multi_dorker.py example.com --gapi-key YOUR_KEY --gapi-cx YOUR_CX --per-query 3 --out example_report.md

    # add include/exclude regex for dorks (applies to generated query text)
    python3 deep_multi_dorker.py example.com --include "swagger|openapi" --exclude "github|stackoverflow"

Note:
 - For non-Google engines (Bing, DuckDuckGo, Yandex) the tool only generates search URLs (manual review).
 - The Google Custom Search JSON API is the only programmatic search path included here; it requires credentials.
 - Be mindful of API quotas and legal scope.

Requirements:
    pip install requests
"""

from __future__ import annotations
import argparse
import urllib.parse
import webbrowser
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys

try:
    import requests
except Exception:
    requests = None  # only required if using Google API; handled later

# ---------------------------
# DORKS (categorised)
# ---------------------------
def generate_dork_map(domain: str) -> Dict[str, List[str]]:
    domain_escaped = domain.strip()
    return {
        "API Endpoints": [
            f"site:{domain_escaped} inurl:api",
            f"site:{domain_escaped} inurl:/api/",
            f"site:{domain_escaped} inurl:v1 OR inurl:v2 OR inurl:v3",
            f"site:{domain_escaped} inurl:graphql",
            f"site:{domain_escaped} inurl:rest OR inurl:api-rest",
            f"site:{domain_escaped} inurl:/internal/api OR inurl:/private/api",
            f"site:{domain_escaped} \"endpoint\"",
            f"site:{domain_escaped} inurl:auth OR inurl:authorize OR inurl:token",
        ],
        "API Documentation": [
            f"site:{domain_escaped} inurl:swagger OR inurl:openapi OR inurl:api-docs",
            f"site:{domain_escaped} filetype:json inurl:swagger",
            f"site:{domain_escaped} filetype:yaml OR filetype:yml \"openapi\"",
            f"site:{domain_escaped} intitle:\"Swagger UI\"",
            f"site:{domain_escaped} intitle:\"API Reference\"",
            f"site:{domain_escaped} \"OpenAPI Specification\"",
            f"site:{domain_escaped} \"swagger.json\" OR \"openapi.json\"",
        ],
        "Exposed Keys & Tokens": [
            f"site:{domain_escaped} ext:env OR ext:ini OR ext:config \"API_KEY\"",
            f"site:{domain_escaped} \"api_key\" OR \"apikey\" OR \"access_token\"",
            f"site:{domain_escaped} \"Authorization: Bearer\"",
            f"site:{domain_escaped} filetype:json \"token\"",
            f"site:{domain_escaped} filetype:js \"apiKey\"",
            f"site:{domain_escaped} \"x-api-key\"",
            f"site:{domain_escaped} \"aws_access_key_id\" OR \"aws_secret_access_key\"",
        ],
        "Debug & Logs": [
            f"site:{domain_escaped} \"debug=true\" OR \"traceback\"",
            f"site:{domain_escaped} intitle:\"index of\" \"logs\"",
            f"site:{domain_escaped} inurl:/logs OR inurl:/debug OR inurl:/error",
            f"site:{domain_escaped} filetype:log",
            f"site:{domain_escaped} \"Exception in thread\"",
            f"site:{domain_escaped} \"stacktrace\" OR \"trace\"",
        ],
        "Cloud & Storage": [
            f"site:s3.amazonaws.com \"{domain_escaped}\"",
            f"site:storage.googleapis.com \"{domain_escaped}\"",
            f"site:blob.core.windows.net \"{domain_escaped}\"",
            f"site:amazonaws.com \"{domain_escaped}\" filetype:json",
            f"site:{domain_escaped} \"bucket\" OR \"s3\"",
            f"site:{domain_escaped} \"cloudfront.net\"",
        ],
        "Config & Backups": [
            f"site:{domain_escaped} ext:xml OR ext:conf OR ext:ini \"password\"",
            f"site:{domain_escaped} filetype:json \"user\" AND \"password\"",
            f"site:{domain_escaped} \"db_password\" OR \"database\" OR \"host\"",
            f"site:{domain_escaped} ext:bak OR ext:old OR ext:backup",
            f"site:{domain_escaped} \"config\" intitle:\"index of\"",
            f"site:{domain_escaped} filetype:env \"SECRET\" OR \"KEY\"",
        ],
        "Tech & Client-side Endpoints": [
            f"site:{domain_escaped} inurl:robots.txt",
            f"site:{domain_escaped} inurl:sitemap.xml",
            f"site:{domain_escaped} filetype:js \"fetch(\" OR \"axios(\" OR \"XMLHttpRequest\"",
            f"site:{domain_escaped} filetype:json \"endpoint\"",
            f"site:{domain_escaped} \"API endpoint\"",
        ],
        "Code & Repository Mentions": [
            f"site:github.com \"{domain_escaped}\" API",
            f"site:gitlab.com \"{domain_escaped}\" inurl:config",
            f"site:pastebin.com \"{domain_escaped}\"",
            f"site:bitbucket.org \"{domain_escaped}\"",
            f"site:jsdelivr.net \"{domain_escaped}\"",
        ],
    }

# ---------------------------
# URL Builders for engines
# ---------------------------
def build_search_url(engine: str, query: str) -> str:
    q = urllib.parse.quote_plus(query)
    if engine == "google":
        return f"https://www.google.com/search?q={q}"
    elif engine == "bing":
        return f"https://www.bing.com/search?q={q}"
    elif engine == "duckduckgo":
        return f"https://duckduckgo.com/?q={q}"
    elif engine == "yandex":
        return f"https://yandex.com/search/?text={q}"
    else:
        raise ValueError("Unsupported engine")

# ---------------------------
# Google Custom Search API wrapper
# ---------------------------
def gcs_fetch(query: str, api_key: str, cx: str, num: int = 3, start: int = 1) -> List[Dict]:
    """
    Fetch top 'num' results for the query using Google Custom Search JSON API.
    Returns list of result dicts with keys: title, snippet, link.
    """
    if requests is None:
        raise RuntimeError("requests library required for Google API calls. Install with: pip install requests")

    results = []
    # API limits max 10 results per request; we request 'num' but enforce 1-10
    num = max(1, min(10, num))
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": num,
        "start": start
    }
    url = "https://www.googleapis.com/customsearch/v1"
    resp = requests.get(url, params=params, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"GCS API HTTP {resp.status_code}: {resp.text}")
    j = resp.json()
    items = j.get("items", [])
    for it in items:
        results.append({
            "title": it.get("title"),
            "snippet": it.get("snippet"),
            "link": it.get("link")
        })
    return results

# ---------------------------
# Filtering helpers (regex)
# ---------------------------
def passes_regex_filters(text: str, include: Optional[re.Pattern], exclude: Optional[re.Pattern]) -> bool:
    if include and not include.search(text):
        return False
    if exclude and exclude.search(text):
        return False
    return True

# ---------------------------
# Markdown report builder
# ---------------------------
def write_markdown_report(filename: str, domain: str, engine_urls: Dict[str, List[Tuple[str,str]]],
                          gcs_results: Optional[Dict[str, List[Dict]]] = None) -> None:
    ts = datetime.utcnow().isoformat() + "Z"
    lines = []
    lines.append(f"# Dorking Report for `{domain}`")
    lines.append(f"_Generated: {ts} (UTC)_\n")
    for engine, tuples in engine_urls.items():
        lines.append(f"## Search URLs ({engine.title()})\n")
        for cat, url in tuples:
            lines.append(f"- **{cat}** — {url}")
        lines.append("")  # newline

    if gcs_results:
        lines.append("## Google Custom Search API Results\n")
        for q, items in gcs_results.items():
            lines.append(f"### Query: `{q}`\n")
            if not items:
                lines.append("_No items returned._\n")
                continue
            for it in items:
                lines.append(f"- [{it.get('title')}]\({it.get('link')}\)  ")
                snippet = (it.get("snippet") or "").replace("\n", " ")
                lines.append(f"  - {snippet}")
            lines.append("")
    # Save
    with open(filename, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"[+] Markdown report saved to {filename}")

# ---------------------------
# CLI / main
# ---------------------------
def parse_args():
    ap = argparse.ArgumentParser(prog="deep_multi_dorker", description="Multi-engine dork generator with optional Google API integration.")
    ap.add_argument("domain", help="Target domain (e.g., example.com)")
    ap.add_argument("--engines", nargs="+", default=["google", "bing", "duckduckgo", "yandex"],
                    help="Search engines to build URLs for (default: google bing duckduckgo yandex)")
    ap.add_argument("--open", action="store_true", help="Open generated URLs in browser tabs (manual review)")
    ap.add_argument("--gapi-key", help="Google Custom Search API key (optional for programmatic querying)")
    ap.add_argument("--gapi-cx", help="Google Custom Search Engine ID (cx) (required if --gapi-key provided)")
    ap.add_argument("--per-query", type=int, default=3, help="Number of top results to fetch per query via Google API (1-10)")
    ap.add_argument("--include", help="Regex to include only dorks that match this pattern (applies to dork text)")
    ap.add_argument("--exclude", help="Regex to exclude dorks that match this pattern (applies to dork text)")
    ap.add_argument("--result-include", help="Regex to include only Google-API results whose title/snippet/link match")
    ap.add_argument("--result-exclude", help="Regex to exclude Google-API results if they match (title/snippet/link)")
    ap.add_argument("--out", help="Markdown output filename (optional)")
    ap.add_argument("--no-open-duplicates", action="store_true", help="Don’t open duplicate URLs when using --open (helps avoid many identical tabs)")
    ap.add_argument("--top-per-category", type=int, default=0, help="If >0, only use the first N dorks per category")
    return ap.parse_args()

def main():
    args = parse_args()
    domain = args.domain

    # compile regex patterns if provided
    include_re = re.compile(args.include, re.IGNORECASE) if args.include else None
    exclude_re = re.compile(args.exclude, re.IGNORECASE) if args.exclude else None
    res_inc_re = re.compile(args.result_include, re.IGNORECASE) if args.result_include else None
    res_exc_re = re.compile(args.result_exclude, re.IGNORECASE) if args.result_exclude else None

    dmap = generate_dork_map(domain)
    engine_urls: Dict[str, List[Tuple[str,str]]] = {e: [] for e in args.engines}
    unique_urls = set()
    gcs_results_all: Dict[str, List[Dict]] = {} if (args.gapi_key and args.gapi_cx) else None

    for cat, queries in dmap.items():
        limited_queries = queries[:args.top_per_category] if args.top_per_category and args.top_per_category>0 else queries
        for q in limited_queries:
            if not passes_regex_filters(q, include_re, exclude_re):
                continue
            for engine in args.engines:
                try:
                    url = build_search_url(engine.lower(), q)
                except ValueError:
                    continue
                engine_urls.setdefault(engine.lower(), []).append((cat, url))
                if args.open:
                    # avoid opening duplicates if requested
                    if args.no_open_duplicates and url in unique_urls:
                        continue
                    try:
                        webbrowser.open_new_tab(url)
                    except Exception as e:
                        print(f"[!] Failed to open browser for {url}: {e}", file=sys.stderr)
                unique_urls.add(url)

            # If Google API credentials are set, fetch results programmatically (respect quota)
            if gcs_results_all is not None:
                try:
                    # fetch top results for this query
                    items = gcs_fetch(q, args.gapi_key, args.gapi_cx, num=args.per_query)
                    # apply result-level regex filters (if any)
                    filtered_items = []
                    for it in items:
                        combined = " ".join(filter(None, [it.get("title",""), it.get("snippet",""), it.get("link","")]))
                        if not passes_regex_filters(combined, res_inc_re, res_exc_re):
                            continue
                        filtered_items.append(it)
                    gcs_results_all[q] = filtered_items
                except Exception as e:
                    print(f"[!] Google API fetch failed for query `{q}`: {e}", file=sys.stderr)
                    gcs_results_all[q] = []

    # Summary print
    total_urls = sum(len(v) for v in engine_urls.values())
    print(f"\n[+] Built {total_urls} search URLs for domain {domain} across engines: {', '.join(args.engines)}")
    if args.open:
        print("[+] Opened search URLs in browser for manual review.")
    if gcs_results_all is not None:
        print(f"[+] Collected programmatic results for {len(gcs_results_all)} queries via Google Custom Search API (subject to quota).")

    # Save markdown if requested
    if args.out:
        write_markdown_report(args.out, domain, engine_urls, gcs_results_all)

    # Also print a short console summary (first 10 URLs)
    print("\nSample URLs (first 10):")
    shown = 0
    for engine, tuples in engine_urls.items():
        for cat, url in tuples:
            print(f"[{engine}] {cat} -> {url}")
            shown += 1
            if shown >= 10:
                break
        if shown >= 10:
            break

if __name__ == "__main__":
    main()
