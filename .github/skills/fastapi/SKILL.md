---
name: fastapi
description: Use for FastAPI routing, Pydantic validation, dependencies, project structure, OpenAPI, status codes and 404/422/500 troubleshooting.
---

# FastAPI learning and diagnosis

Explain the HTTP request lifecycle, routers, path/query/body inputs, Pydantic request/response models, dependency injection, validation, OpenAPI and Swagger UI, common status codes and exception handling.

Discuss project structure and separation of routers, services, repositories, schemas and application configuration. Explain how FastAPI relates to SQLAlchemy, HTTPX and test clients; diagnose imports and circular dependencies conceptually.

**Method:** identify which layer fails → inspect the actual student-written route/schema and request → suggest one focused check → let the student implement the fix.

**Boundary:** never write or rewrite routes, validators, dependency functions, services, models, complete scaffolds or implementation patches. For complete route tests, use **testing**.

**Example prompts:** “Why does this JSON return a 422?” and “How should responsibilities be divided between routers and services?”
