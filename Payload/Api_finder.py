#!/usr/bin/env python3
"""
deep_api_dorker.py

Passive OSINT tool that generates advanced Google Dorks to discover
API endpoints, documentation, and potential configuration leaks.

Usage:
    python3 deep_api_dorker.py example.com
    python3 deep_api_dorker.py example.com --open
    python3 deep_api_dorker.py example.com --save dorks.txt
"""

import sys
import urllib.parse
import webbrowser
from datetime import datetime

def generate_dorks(domain):
    """Generate categorized dorks."""
    dorks = {
        "API Endpoints": [
            f"site:{domain} /swagger/index.html",
            f"site:{domain} api",
            f"site:{domain} inurl:api",
            f"site:{domain} inurl:/api/",
            f"site:{domain} inurl:v1 OR inurl:v2 OR inurl:v3",
            f"site:{domain} inurl:rest OR inurl:graphql",
            f"site:{domain} inurl:/dev/api OR inurl:/staging/api",
            f"site:{domain} inurl:/internal/api OR inurl:/private/api",
        ],

        "API Documentation": [
            f"site:{domain} inurl:swagger OR inurl:openapi OR inurl:api-docs",
            f"site:{domain} filetype:json inurl:swagger",
            f"site:{domain} filetype:yaml OR filetype:yml \"openapi\"",
            f"site:{domain} intitle:\"Swagger UI\"",
            f"site:{domain} intitle:\"API Reference\"",
            f"site:{domain} \"OpenAPI Specification\"",
        ],

        "Exposed Keys & Tokens": [
            f"site:{domain} ext:env OR ext:ini OR ext:config \"API_KEY\"",
            f"site:{domain} \"api_key\" OR \"apikey\" OR \"access_token\"",
            f"site:{domain} \"Authorization: Bearer\"",
            f"site:{domain} filetype:json \"token\"",
            f"site:{domain} filetype:js \"apiKey\"",
            f"site:{domain} \"x-api-key\"",
        ],

        "Debug & Logs": [
            f"site:{domain} \"debug=true\" OR \"traceback\"",
            f"site:{domain} intitle:\"index of\" \"logs\"",
            f"site:{domain} intitle:\"index of\" \"error\"",
            f"site:{domain} inurl:/logs OR inurl:/debug",
            f"site:{domain} filetype:log",
            f"site:{domain} \"Exception in thread\"",
        ],

        "Cloud & Storage Leaks": [
            f"site:s3.amazonaws.com \"{domain}\"",
            f"site:storage.googleapis.com \"{domain}\"",
            f"site:blob.core.windows.net \"{domain}\"",
            f"site:amazonaws.com \"{domain}\" filetype:json",
            f"site:{domain} \"bucket\" OR \"aws_access_key_id\"",
            f"site:{domain} \"cloudfront.net\"",
        ],

        "Configuration Files": [
            f"site:{domain} ext:xml OR ext:conf OR ext:ini \"password\"",
            f"site:{domain} filetype:json \"user\" AND \"password\"",
            f"site:{domain} \"db_password\" OR \"database\" OR \"host\"",
            f"site:{domain} ext:bak OR ext:old OR ext:backup",
            f"site:{domain} \"config\" intitle:\"index of\"",
        ],

        "Web & App Tech": [
            f"site:{domain} inurl:robots.txt",
            f"site:{domain} inurl:sitemap.xml",
            f"site:{domain} filetype:js \"fetch(\" OR \"axios\"",
            f"site:{domain} filetype:json \"endpoint\"",
            f"site:{domain} \"API endpoint\"",
        ],

        "Code & Git Leaks": [
            f"site:github.com \"{domain}\" API",
            f"site:gitlab.com \"{domain}\" inurl:config",
            f"site:pastebin.com \"{domain}\"",
            f"site:bitbucket.org \"{domain}\"",
            f"site:jsdelivr.net \"{domain}\"",
        ]
    }

    return dorks


def encode_query(q):
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(q)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 deep_api_dorker.py <domain> [--open] [--save file]")
        sys.exit(1)

    domain = sys.argv[1]
    do_open = "--open" in sys.argv
    save_file = None
    if "--save" in sys.argv:
        try:
            save_file = sys.argv[sys.argv.index("--save") + 1]
        except IndexError:
            print("Error: specify file after --save")
            sys.exit(1)

    dork_map = generate_dorks(domain)
    output_lines = []
    total = 0

    print(f"\n[+] Generating advanced Google Dorks for {domain}\n")
    for category, queries in dork_map.items():
        print(f"=== {category} ===")
        for q in queries:
            url = encode_query(q)
            print(f"\nDORK: {q}\nURL:  {url}\n")
            output_lines.append(f"[{category}] {q}\n{url}\n")
            total += 1
            if do_open:
                webbrowser.open_new_tab(url)

    print(f"\n[+] Generated {total} total dorks.\n")

    if save_file:
        with open(save_file, "w") as f:
            f.write(f"# Dorks generated for {domain} - {datetime.now()}\n\n")
            f.write("\n".join(output_lines))
        print(f"[+] Saved all dorks to {save_file}\n")


if __name__ == "__main__":
    main()
