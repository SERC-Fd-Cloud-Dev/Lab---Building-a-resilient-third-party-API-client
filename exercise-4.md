# Exercise 4 — Apply cache-backed fallback

Distinguish usable stale data from data too old to serve.

**Time:** 20 minutes. **Work:** individual, compare reasoning with a partner after checking.


## Before you start

Complete Exercise 3. An availability estimate can remain useful briefly during an outage, but it must carry its age and cannot guarantee stock. This example permits fresh data for less than 10 seconds and retains it for fallback until 60 seconds. Those thresholds are teaching policy choices, not recommended production defaults.

## Guided walkthrough

Read `app/cache_policy.py` and the call to `may_fallback` in `service.py`. The service already stores successful responses and labels `source`, `stale` and `age_seconds`. It also removes entries at the retention boundary.

Predict whether an entry aged 9, 10, 59 and 60 seconds is fresh, stale-but-retained or unusable.

## Guided application

Implement `may_fallback(entry, now, error)`. Return true only when an entry exists, `error.fallback` permits this failure category and its age is between zero (inclusive) and `RETAIN_SECONDS` (exclusive).

## Supported practice

Run `python -m pytest tests/verification/test_fallback.py -q`. Expect **3 passes**. The fake clock verifies exact boundaries without waiting. Check that a stale fallback still increments the breaker and that an open breaker can use retained data without a new upstream attempt.

## Required decision

Explain why a cached stock estimate may be appropriate for browsing but inappropriate for confirming a purchase. Predict what happens when the supplier and the cache are both unavailable. A controlled error is a valid result; fabricated stock is not.

**Evidence:** a passing retention-boundary test, a labelled fallback response and two sentences justifying the policy. Optional: add a test for a future-dated cache entry.

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
