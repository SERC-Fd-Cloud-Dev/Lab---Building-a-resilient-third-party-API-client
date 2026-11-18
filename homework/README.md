# Homework — Making the Movie Guessing Game more resilient

**Time:** approximately 60 minutes. Work independently in this supplied starter. No code from earlier weeks is required. The game already supplies a public clue and a protected answer. TMDB communication belongs in `movie_game/services/tmdb.py`; keep routes separate from the integration.

## Start and check — 10 minutes

From the repository root with `.venv` activated:

```bash
cd homework
python -m pytest -q
python -m uvicorn movie_game.main:app --host 0.0.0.0 --port 8001
```

Expect **2 baseline passes**. Open private port 8001 at `/docs`. Offline mode is the default and uses a synthetic movie fixture. `GET /games/11/clue` returns year and runtime. The answer needs `X-API-Key: local-practice-only`. This key is an explicitly public local teaching value; use your own environment value for live practice and keep `.env` untracked.

Read [the endpoint and data contract](../API-CONTRACT.md). Trace route → service → HTTPX. Explain why a GET can usually be retried safely and why that does not permit unlimited attempts.

## Implement — 20 minutes

Modify `TMDBService.movie` only, adding imports/helpers in the same service module if needed:

- Three total attempts for `TMDBFailure.retryable` failures, with backoff 0.1 then 0.2 seconds.
- Return immediately after success; re-raise non-retryable and exhausted failures.
- Use the injected `self.sleep` for deterministic tests.
- Emit safe JSON events through logger `movie_game`, including the supplied request ID and attempt count. Do not log credentials, headers, full URLs or movie response bodies.
- Preserve all routes, clue/answer shapes and authentication. Missing/wrong incoming key must result in zero TMDB requests.

## Verify — 20 minutes

Run `python -m pytest tests verification -q`. The supplied checks exercise transient recovery, exhausted errors, permanent errors, safe logs and credential separation. They initially fail on the missing retry/logging behaviour. Expect **8 passes** for a completed reference implementation.

Add at least one test of your own, such as a timeout followed by success, or invalid 200 data. Verify call counts, not only final status. Use HTTPX `MockTransport`; no live TMDB account is needed. Explain what mocks establish and what they cannot establish about a real supplier.

## Explain — 10 minutes

Bring your test output, one safe log sequence and 100–150 words explaining:

1. Which failures you retry and why repeating this read is acceptable.
2. What the caller receives when attempts are exhausted or a permanent failure occurs.
3. How you verified that access control still runs before the TMDB call.

## Self-check

- I can explain the distinction between the game key and TMDB token.
- I implemented bounded attempts with no delay after the final failure.
- I preserved the public clue and protected answer.
- I wrote and ran a meaningful extra mocked test.
- My evidence contains no credentials or full credential-bearing URLs.

## Hints and recovery

<details><summary>Hint 1</summary>Use the classroom retry structure, but keep all TMDB work inside the service module.</details>
<details><summary>Hint 2</summary>`_once` already translates transport, HTTP and validation failures to `TMDBFailure`. The retry loop should use its policy flag.</details>
<details><summary>Hint 3</summary>Count attempts from 1 to 3. On failure stop when `not error.retryable` or the count is 3; otherwise record and await the backoff.</details>

If imports fail, run from `homework/`. If an authentication test causes an upstream call, check the route dependency before changing the service. If a live token is unavailable, keep offline mode; it is sufficient for all core work. Save your work before examining `solutions/homework` in the full distribution.

## Optional live TMDB check

Copy `.env.example` to `.env`, set `TMDB_MODE=live`, supply your TMDB API Read Access Token as `TMDB_READ_TOKEN`, and set a separate `GAME_API_KEY`. Restart the server. Use a movie ID available in TMDB. The synthetic offline title is not a claim about that live ID. Follow [TMDB application authentication](https://developer.themoviedb.org/docs/authentication-application) and its usage/attribution requirements. Tests remain mocked; do not inject deliberate faults or repeated load against TMDB.

## Optional extension

Apply a circuit-breaker package to this service and verify failure counting and recovery. This is outside the one-hour core task. The supplied possible solution covers the required homework; the classroom breaker solution provides a transferable example.

[Back to lab](../README.md)
