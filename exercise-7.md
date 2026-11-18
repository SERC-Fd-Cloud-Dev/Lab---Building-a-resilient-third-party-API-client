# Exercise 7 — Investigate Redis caching

Extend the completed application with an external cache and test cache failure.

**Time:** 40 minutes. **Work:** individual, compare reasoning with a partner after checking.


## Optional extension

This task is separate from core completion and homework. Complete Exercise 6 first. Docker is used as supplied infrastructure; authoring containers is taught later.

## Guided setup

```bash
docker info
docker compose -f optional-redis/compose.yaml up -d --wait
docker compose -f optional-redis/compose.yaml exec redis redis-cli ping
cp optional-redis/redis_cache.py app/redis_cache.py
CACHE_BACKEND=redis python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`PING` should return `PONG`. Stop any other process on port 8000 first. The supplied Redis adapter uses bounded connection/read timeouts and treats Redis errors as cache misses/write failures. It does not fall back to a hidden second cache.

## Supported investigation

Fetch `drill-01`, wait until the data is stale (at least 10 seconds), set `unavailable` and fetch again before 60 seconds elapse. Expect labelled fallback. Inspect the stored TTL:

```bash
docker compose -f optional-redis/compose.yaml exec redis redis-cli TTL availability:drill-01
```

The retention TTL starts at 60 seconds, not 10. It keeps stale data available for the fallback window. Stale reads do not refresh TTL. Explain what would happen if TTL were only the freshness duration.

## Required investigation within this optional task

Stop Redis using `docker compose -f optional-redis/compose.yaml stop redis`. With an available supplier, the API should still retrieve live data; with both unavailable and no cache, it should return a controlled error. Reset the lab before comparisons so an already-open breaker does not obscure the result.

Run `python -m pytest tests/verification/test_redis.py -q`. Expect **2 passes** using a fake Redis client. These tests check the adapter and retention policy; they do not establish that Docker or a real Redis daemon is available. Record the separate `PONG`, TTL and stopped-container observations.

## Reflection and cleanup

Compare sharing cached data between workers with the extra network dependency it introduces. Explain why a shared cache does not make each process's circuit breaker shared.

```bash
docker compose -f optional-redis/compose.yaml down
```

The supplied container has no persistent volume. The optional solution contains the complete adapter and reference investigation.

## Finish and reflect

- Save your code and test output. Explain one prediction that the results confirmed or changed.
- Commit the completed change, then continue to the next exercise from the lab overview.
- If a test fails, read its first failed assertion, inspect the relevant hook and rerun that file. Keep your current work before using a checkpoint in a new directory.

## Support

<details><summary>Hint 1: identify the boundary</summary>
Which part is responsible for the behaviour: the HTTP attempt, retry operation, breaker, cache or route? Follow that boundary before editing.
</details>

<details><summary>Hint 2: inspect evidence</summary>
Compare the expected attempt count, API response and failure category. A successful response alone does not prove the resilience policy worked.
</details>

<details><summary>Hint 3: reduce the case</summary>
Run a single test with `python -m pytest path/to/test_file.py -x -vv`, replacing the path with this exercise's stated test file. Check the function named in the failure before changing unrelated code.
</details>

| Symptom | Check | Recovery |
|---|---|---|
| Import error | Working directory and activated `.venv` | Run from the repository root using `python -m pytest` |
| Unexpected cached success | `/lab/state`, cache age | `POST /lab/reset`, then set the scenario again |
| Breaker rejects a request | Current state and previous failed calls | Reset the lab or wait for the configured recovery interval |
| Edit has no visible effect | Running server | Stop with Ctrl+C and restart the stated Uvicorn command |
| Test expects more behaviour than implemented | Selected verification file | Use only the current and already-completed stage tests |

**Catch-up:** use the tutor-supplied previous checkpoint in a new folder, complete this stage's small change and explain its targeted test. A terminal and the same tests provide an alternative to Postman or Swagger UI.

[Return to the lab overview](README.md)
