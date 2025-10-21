# BSCP — 4‑Week Study Plan (daily tasks) + 30 recommended PortSwigger labs

**Goal:** Prepare to pass the Burp Suite Certified Practitioner by building hands-on fluency with Burp + PortSwigger labs, evidence collection, and reporting. This plan assumes ~2–4 hrs/day on weekdays and 4–6 hrs on weekend days.

---

## Quick rules for every session
- Work with Burp Proxy on; save HTTP history and use Repeater/Intruder often.  
- For blind/OOB issues, use Burp Collaborator and take screenshots of Collaborator hits.  
- For each lab: capture request, response, proof string, and a 1-paragraph reproduction step. Save screenshots named `weekX_dayY_topic_labname.png`.

---

## Week 1 — Foundations + XSS + CSRF

**Day 1 — Burp basics & scanning workflow**
- Read Burp quickstart: proxy, Repeater, Target map, Scanner basics.  
- Hands-on: map a simple site in Proxy; practice sending requests to Repeater/Intruder.

**Day 2 — Reflected XSS (apprentice)**
- Labs: Reflected XSS into HTML context.  
- Lab: Reflected XSS into HTML context with nothing encoded — try payloads in search.  
  (Lab: https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)

**Day 3 — DOM XSS & stored variants**
- Labs: Reflected DOM XSS, Stored DOM XSS. Practice finding JS sinks and using encoded payloads.  
  (Reflected DOM XSS: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected)  
  (Stored DOM XSS: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored)

**Day 4 — Stored XSS & exploiting impacts**
- Labs: Stored XSS into HTML context (post comments), stealing cookies and passwords labs.  
  (Stored XSS: https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded)  
  (Capture passwords: https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-capturing-passwords)  
  (Steal cookies: https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-stealing-cookies)

**Day 5 — CSRF basics + chaining with XSS**
- Labs: CSRF vulnerability with no defenses; CSRF where token is not tied to session; CSRF token depends on method; Exploiting XSS to bypass CSRF.  
  (CSRF no defenses: https://portswigger.net/web-security/csrf/lab-no-defenses)  
  (Token not tied: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-not-tied-to-user-session)  
  (Token depends on method: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-validation-depends-on-request-method)  
  (XSS -> CSRF: https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-perform-csrf)

**Weekend — Reporting practice & timed mini-mock**
- Write 2 short reports from the week (one XSS, one CSRF). Time a 2-hour mini mock: solve any 2 labs and produce evidence.

---

## Week 2 — Auth, JWT, Request Smuggling, Host header

**Day 8 — Auth flows, session management**
- Learn: session fixation, session handling rules in Burp, macros for login. Practice replaying auth flows.

**Day 9 — JWT attacks (theory + labs)**
- Labs: JWT algorithm confusion; JWT auth bypass via unverified signature.  
  (Algorithm confusion: https://portswigger.net/web-security/jwt/algorithm-confusion)  
  (Unverified signature lab: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature)

**Day 10 — Brute force & authentication misconfigurations**
- Practice Burp Intruder credential stuffing (rate-limit awareness), account lockout testing, and measuring response differences.

**Day 11 — HTTP request smuggling (core practice)**
- Labs: Basic CL.TE and basic TE.CL labs. Practice detecting via timing and using Proxy + Repeater.  
  (CL.TE: https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te)  
  (TE.CL: https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl)

**Day 12 — Host header & web cache poisoning basics**
- Practice host header manipulation, caching interactions, and evidence capture. Explore Web Cache Deception learning path if time.

**Weekend — Timed lab + Collaborator practice**
- 3-hour session: solve 2 labs from this week (one JWT, one smuggling). Practice Burp Collaborator setup and screenshots.

---

## Week 3 — APIs, SSRF, SSTI, File Uploads

**Day 15 — API testing basics & GraphQL**
- Learn API auth flows, testing endpoints, parameter pollution. Lab: Performing CSRF exploits over GraphQL.  
  (GraphQL CSRF: https://portswigger.net/web-security/graphql/lab-graphql-csrf-via-graphql-api)

**Day 16 — SSRF fundamentals**
- Lab: Basic SSRF against the local server. Practice internal target enumeration and chaining to admin endpoints.  
  (SSRF basic: https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost)

**Day 17 — XXE & blind XXE**
- Labs: Blind XXE with OOB interaction; parameter-entities variant. Practice Burp Collaborator DNS/HTTP OOB.  
  (Blind XXE OOB: https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction)  
  (Parameter entities: https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction-using-parameter-entities)

**Day 18 — SSTI (Server-side template injection)**
- Labs: Basic SSTI (ERB) and SSTI (Tornado code context). Learn common payloads for ERB/Jinja/Tornado.  
  (SSTI ERB: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic)  
  (SSTI Tornado: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-code-context)

**Day 19 — File upload exploitation**
- Labs: Web shell upload via Content-Type restriction bypass; web shell upload via extension blacklist bypass. Practice bypass techniques (magic bytes, double extensions, alternate paths).  
  (Content-Type bypass: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass)  
  (Extension blacklist bypass: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass)

**Weekend — Chaining day**
- Choose one chaining exercise: SSRF→RCE, SSTI→file read, Upload→web shell. Produce full evidence and a short report.

---

## Week 4 — LFI/RCE, Deserialization, SQLi, Business Logic & Mock Exams

**Day 22 — SQL Injection deep dive**
- Labs: SQL injection login bypass; retrieve hidden data. Practice boolean/time-based blind techniques and UNION attacks.  
  (Login bypass: https://portswigger.net/web-security/sql-injection/lab-login-bypass)  
  (Retrieve hidden data: https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)

**Day 23 — Insecure deserialization (hands-on)**
- Labs: Modifying serialized objects; PHP deserialization pre-built; Java Apache Commons exploit. Practice using ysoserial and pre-built gadget chains.  
  (Modify objects: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)  
  (PHP pre-built: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-php-deserialization-with-a-pre-built-gadget-chain)  
  (Java Apache Commons: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons)

**Day 24 — Path traversal & LFI**
- Labs: File path traversal simple case; traversal sequences blocked; validation-of-start-of-path. Practice encoding and null-byte techniques.  
  (Simple case: https://portswigger.net/web-security/file-path-traversal/lab-simple)  
  (Traversal blocked absolute path bypass: https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass)  
  (Validation start of path: https://portswigger.net/web-security/file-path-traversal/lab-validate-start-of-path)

**Day 25 — OS command injection & privilege escalation**
- Practice typical command injection payloads, escaping, and chaining to read files or spawn shells.

**Day 26 — Business logic, race conditions, and reporting**
- Tackle 2 business-logic style labs (mimic real-world flows), attempt a race condition lab if available, and practice concise reporting.

**Day 27–28 — Mock exam weekend**
- Full timed mock: 6–8 hours simulating exam. Attempt to solve 4–6 labs of mixed difficulty. Produce 4 reports.

---

## 30 Recommended Labs (direct links)
1. HTTP request smuggling, basic CL.TE — https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te
2. HTTP request smuggling, basic TE.CL — https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl
3. Algorithm confusion attacks (JWT) — https://portswigger.net/web-security/jwt/algorithm-confusion
4. JWT authentication bypass via unverified signature — https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature
5. Reflected XSS into HTML context with nothing encoded — https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded
6. Reflected DOM XSS — https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected
7. Stored XSS into HTML context with nothing encoded — https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded
8. Stored DOM XSS — https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored
9. CSRF vulnerability with no defenses — https://portswigger.net/web-security/csrf/lab-no-defenses
10. CSRF where token is not tied to user session — https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-not-tied-to-user-session
11. CSRF where token validation depends on request method — https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-validation-depends-on-request-method
12. Exploiting XSS to bypass CSRF defenses — https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-perform-csrf
13. SQL injection vulnerability allowing login bypass — https://portswigger.net/web-security/sql-injection/lab-login-bypass
14. SQL injection in WHERE clause allowing retrieval of hidden data — https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data
15. Basic SSRF against the local server — https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost
16. Blind XXE with out-of-band interaction — https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction
17. Blind XXE using parameter entities — https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction-using-parameter-entities
18. Basic server-side template injection (ERB) — https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic
19. Basic server-side template injection (Tornado code context) — https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-code-context
20. Web shell upload via Content-Type restriction bypass — https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass
21. Web shell upload via extension blacklist bypass — https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass
22. Modifying serialized objects — https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects
23. Exploiting PHP deserialization with a pre-built gadget chain — https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-php-deserialization-with-a-pre-built-gadget-chain
24. Exploiting Java deserialization with Apache Commons — https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons
25. File path traversal, simple case — https://portswigger.net/web-security/file-path-traversal/lab-simple
26. File path traversal, traversal sequences blocked with absolute path bypass — https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass
27. File path traversal, validation of start of path — https://portswigger.net/web-security/file-path-traversal/lab-validate-start-of-path
28. Exploiting XSS to capture passwords — https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-capturing-passwords
29. Exploiting XSS to steal cookies — https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-stealing-cookies
30. Mystery lab challenge (timed practice) — https://portswigger.net/web-security/all-labs

---

## Final checklist before exam
- Burp configured: Proxy, Collaborator active, history saved.  
- Have pre-made templates for evidence & reports (1-paragraph vuln + steps + evidence).  
- Practice 2 full timed mocks (at least one 6–8 hrs).  
- Sleep well the night before — fresh brain helps pattern recognition.

---

If you'd like, I can now:
- Export this plan into a printable PDF or Google Calendar invite set; or
- Convert this into a day-by-day checklist with checkboxes you can tick in the canvas.

Which would you like next?

