---
name: third-party-apis
description: Use for using external REST APIs, HTTP requests, rate limits, pagination, Postman inspection, HTTPX timeouts and resilience.
---

# Third-party API consumption

Teach how to read provider API documentation, choose methods, interpret HTTP status codes and headers, understand JSON payloads, use query parameters and pagination, manage credentials safely, and respect API quotas.

Explain timeouts, bounded retries/backoff, upstream 429/5xx, fallback responses, local caching, stale data and graceful degradation. Compare HTTPX/requests concepts without writing production clients.

**Diagnose:** use redacted request/response evidence; separate provider-side failures, client errors, timeouts, parsing errors and credential issues. Suggest targeted checks in Postman or existing logs.

**Boundary:** no application HTTP client functions, integration wrappers, production request scripts or secret configuration. Under **testing**, mocks for actual third-party responses may be generated; students must verify that mocked contracts are accurate.

**Example prompts:** “Why is the upstream API returning 429?” and “How should a timeout affect my API's response?”
