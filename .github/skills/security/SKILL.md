---
name: security
description: Use for API authentication, authorisation, roles, resource ownership, secrets handling, CORS, logging and OWASP API Security.
---

# API security concepts

Explain authentication vs authorisation, API keys vs bearer tokens, ownership checks, least privilege, threat boundaries, safe configuration, secrets management, CORS, rate limiting and secure logs.

Ask the student to distinguish unauthenticated (401), authenticated-but-forbidden (403) and allowed requests, and to consider which resources each identity may access.

Use the student's existing code or redacted responses for diagnostic explanations. Consider abuse cases and appropriate tests.

**Boundary:** never generate security middleware, token-handling code, access-control implementations or application configuration. Under **testing**, complete tests of existing protected endpoints and access rules are permitted.

Never request actual secrets or include them in tests or documentation.
