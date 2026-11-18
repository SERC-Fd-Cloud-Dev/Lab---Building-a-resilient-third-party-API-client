# Exercise 5 — Record structured diagnostic events

Create safe records that let you reconstruct one request.

**Time:** 10 minutes. **Work:** individual, compare reasoning with a partner after checking.


## Before you start

Complete Exercise 4. The application already emits events at meaningful boundaries and generates a request ID. Your small task is to implement the formatter/output hook in `app/observability.py`, not to build a logging framework.

## Guided walkthrough

Read `ALLOWED`. Explain why `request_id`, `attempt`, `delay` and a fixed error `kind` help diagnosis, while arbitrary URLs, headers and response bodies may reveal secrets.

## Guided application

In `event`, create a dictionary with a UTC ISO timestamp, level name and event name. Add only fields whose keys are in `ALLOWED`. Use `json.dumps` and `logger.log` to emit one JSON record per line. Use WARNING for retries/fallback, ERROR when the outward request fails, and INFO for normal progress. CRITICAL is for severe application-wide failure, not every dependency error.

## Supported check

Run `python -m pytest tests/verification/test_logging.py -q`. Expect **2 passes**. The safe-field test passes credential-like data deliberately and expects it to be excluded. It does not claim to detect every possible secret: production logging also requires review of the allowed values.

## Required interpretation

Trigger `flaky` after a reset. Identify attempt 1, scheduled retry, attempt 2 and success sharing one request ID. State the original failure and final response. Logs describe events; use response/test evidence as well before claiming the behaviour is correct.

**Evidence:** a short safe sequence and an explanation. Keep this change small to protect the independent investigation time.

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
