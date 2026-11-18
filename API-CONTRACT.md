# Endpoints and data shapes

The starter and completed applications share these routes. Completion adds resilience without changing successful response shapes. All JSON requests use `Content-Type: application/json`.

## Workshop Supplies API

| Method and path | Input | Success shape | Errors / behaviour |
|---|---|---|---|
| `GET /health` | None | `200 {"status":"ok"}` | Process health only; not supplier readiness |
| `GET /availability/{sku}` | Path string; supplied example `drill-01` | `200 Availability` below | Supplier not found → 404; invalid/rejected supplier response → 502; connection/exhausted 5xx/open circuit → 503; timeout → 504 |
| `PUT /lab/scenario` | `{"scenario":"flaky"}` | `200 {"scenario":"flaky","calls":0}` | Invalid scenario → 422; resets transport counter only, preserves cache/breaker |
| `GET /lab/state` | None | `200 {"scenario":"success","upstream_calls":1,"breaker":"closed","failure_count":0}` | Starter breaker value is `disabled` |
| `POST /lab/reset` | No body | `200 {"reset":true}` | Clears `drill-01` cache, resets breaker and simulator; lab only |

No classroom endpoint requires credentials. The `/lab/*` controls are for private local practice, not deployment. The simulator returns a drill fixture; use the documented SKU. It is not a full inventory database.

### Availability

```json
{
  "product": {"sku":"drill-01","name":"Cordless drill","available":7},
  "source":"upstream",
  "stale":false,
  "age_seconds":0.0
}
```

| Field | Type | Meaning / constraint |
|---|---|---|
| `product.sku` | string | Must match the requested SKU |
| `product.name` | string | Display name |
| `product.available` | integer ≥ 0 | Supplier-reported quantity; not a reservation guarantee |
| `source` | string | `upstream`, `cache` or `fallback` |
| `stale` | boolean | True when age is at least 10 seconds |
| `age_seconds` | number ≥ 0 | Age since this response was fetched, rounded to 3 decimals |

Fresh cache: age `<10s`; stale but retained: `10s ≤ age <60s`; unusable: age `≥60s`. Only temporary dependency failures or an open circuit permit fallback. A 404, upstream authentication rejection or invalid payload cannot silently become cached success. All responses carry a generated `X-Request-ID`.

### Controlled upstream error

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/problem+json
X-Request-ID: 4d473534-9b0f-4a21-b08a-8f2b2e7cd001
```

```json
{
  "type":"about:blank",
  "title":"Service Unavailable",
  "status":503,
  "detail":"The upstream service is temporarily unavailable.",
  "instance":"urn:uuid:4d473534-9b0f-4a21-b08a-8f2b2e7cd001"
}
```

The ID above is illustrative. `instance` identifies this occurrence; `type` identifies the problem category. The HTTP status is authoritative and matches `status`. These are the upstream error responses, not a claim that every framework-generated error uses RFC 9457: FastAPI's request-validation 422 retains its standard `detail` list.

### Simulator modes

| Mode | Supplier behaviour |
|---|---|
| `success` | Valid 200 product |
| `flaky` | First call 503, subsequent calls 200 |
| `timeout` | Injected HTTPX `ReadTimeout` |
| `connection` | Injected HTTPX `ConnectError` |
| `unavailable` | Always 503 |
| `invalid` | 200 with invalid product shape |
| `missing` | 404 |
| `unauthorised` | Upstream 401, unrelated to the caller's identity |
| `rate-limit` | 429 with `Retry-After: 20`; investigate in Exercise 6 |

The intended completed policy for supplier 429 is one attempt, no breaker failure, no fallback and a controlled API 503. The upstream limit applies to the integration's shared quota, not necessarily this caller. The lab does not sleep 20 seconds inside an interactive request or blindly forward the upstream header. A production design could queue work, schedule a later attempt or enforce a validated retry window with an explicit time budget.

## Homework Movie Guessing Game

| Method and path | Input / authentication | Success shape | Errors |
|---|---|---|---|
| `GET /games/{movie_id}/clue` | Integer movie ID; public | `200 {"movie_id":11,"year":"2001","runtime_minutes":112}` | 404 / 502 / 503 / 504 upstream; invalid path → 422 |
| `GET /games/{movie_id}/answer` | Integer ID and `X-API-Key` matching `GAME_API_KEY` | `200 {"movie_id":11,"title":"The Clockwork Moon"}` | Missing/wrong key → 401 **before TMDB is called**; upstream errors as above |

The fixture is synthetic, not TMDB data. Offline mode only supplies movie ID 11. Clues omit the title. Using a public TMDB ID is an intentional classroom simplification: authentication protects this API's answer endpoint but cannot prevent someone looking up the public movie elsewhere.

TMDB service data shape: `id` integer, `title` string, `release_date` string, `runtime` positive integer. Routes call `movie_game/services/tmdb.py`; routes never issue HTTP requests. Live mode sends `TMDB_READ_TOKEN` as a Bearer token to `https://api.themoviedb.org/3/movie/{movie_id}`. This credential is distinct from the incoming game key.

The game translates upstream errors to Problem Details. Its authentication 401 retains FastAPI's `{"detail":"Valid game API key required"}` shape. Existing response contracts and protection must remain unchanged.
