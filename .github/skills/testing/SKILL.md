---
name: testing
description: Use when designing or generating unit, integration, API, contract, negative, authorisation and security tests; pytest, FastAPI TestClient, fixtures and mocks.
---

# Automated testing — executable tests permitted

**This is an explicit exception to the no-implementation-code policy.** You may generate complete unit and integration tests (including pytest/FastAPI TestClient), test-only fixtures, mocks, parametrised cases, negative/boundary tests, and tests for API contracts, authentication, CRUD and upstream failures. Related Postman **test scripts** are permitted.

## Workflow

1. Read real student-written application interfaces and any existing tests. Establish student-defined expected behaviour; distinguish unknowns.
2. Select the correct boundary (unit vs integration) and explain Arrange–Act–Assert.
3. Define meaningful positive, negative, boundary and authorisation cases with unambiguous assertions.
4. Write **only** test-specific code in the existing/agreed test paths; isolate external services and use disposable data where appropriate.
5. Explain what each test demonstrates, expected failures and possible false confidence.
6. Ask the student to run, review, interpret and refine the generated tests. Do not invent results.

**Never** create or modify app routes, services, ORM models, validators, dependency manifests, workflows, auth implementations or deployment settings. Never weaken an assertion to hide a defect. If the tested app is broken, explain why and let the student fix it.

Ask students to review generated tests and understand what they verify.

**Example prompts:** “Generate pytest tests for the endpoints I already wrote, including 401 and 403 cases” and “Why does this integration test fail?”
