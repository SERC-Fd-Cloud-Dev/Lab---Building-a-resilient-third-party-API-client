# Exercise 1 — Observe and classify failures

Read the running application and separate supplier failure from API response.

**Time:** 15 minutes. **Work:** individual, compare reasoning with a partner after checking.


## Before you start

Complete the README setup. Inspect `app/main.py`, `app/service.py` and `app/supplier.py`. The route handles the caller; the service handles the dependency. Read the endpoint contract before sending requests.

## Guided walkthrough

1. Open `/docs`. Run `POST /lab/reset` and `GET /availability/drill-01`.
2. Predict whether the next identical request will reach the supplier. Run it, then inspect `GET /lab/state`.
3. Expect the second response to say `source: cache` and the counter to stay at 1. Explain what the cache has avoided.
4. Reset, then run `PUT /lab/scenario` with `{"scenario":"timeout"}`. Request availability again. Expect 504 and `application/problem+json`.

## Supported investigation

Try `connection`, `unavailable`, `invalid` and `unauthorised`. Reset before each. Record supplier behaviour, outward status and counter. The starter makes one attempt; the total-operation guard is supplied, but narrower HTTPX phase limits are not yet configured.

## Required decision

Predict the result of `flaky` before running it. Explain why a safe, bounded second attempt might help and why the same decision would be unsafe for an unprotected payment operation. Keep a three-row failure table and your explanation.

**Check:** `python -m pytest -q` → 3 baseline tests pass. The flaky starter call returns 503; it makes one attempt. No code change is required in this orientation.

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
