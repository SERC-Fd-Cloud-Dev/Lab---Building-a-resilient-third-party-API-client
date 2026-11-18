# Exercise 6 — Investigate a rate-limited dependency

Independently decide, implement and verify a new failure policy.

**Time:** 25 minutes. **Work:** individual, compare reasoning with a partner after checking.


## Starting point

Complete Exercises 2–5 or use the tutor's Exercise 5 checkpoint in a new folder. The simulator has a `rate-limit` mode that returns upstream 429 with `Retry-After: 20`. The integration uses a shared supplier quota. The interactive API request has a two-second upstream-operation budget.

## Guided diagnostic start

Reset the lab, select `rate-limit`, request `drill-01` and inspect the response and log sequence. The current mapping returns 502. Reproduce this before making changes. Recall that an upstream 401 or 429 is not automatically an authentication or rate-limit error attributable to this API's caller.

## Required independent task

Make and justify the policy in `app/errors.py` and your own tests:

- The API returns a controlled **503 Problem Details** response for this supplier-wide quota limit.
- It makes **one** upstream attempt, does not wait 20 seconds and does not add a breaker failure.
- It does not substitute retained stock data for this policy case.
- Safe logs identify the category and correlate with the response ID.
- Existing retry, breaker, fallback and authentication behaviour stays intact.

Explain whether a later queued retry could be safe for this GET and what additional scheduling/rate-limit policy it would need. You do **not** need to implement a queue, parse HTTP-date `Retry-After`, or create an idempotency-key mechanism.

## Verification

Run `python -m pytest tests/verification/test_independent.py -q`. This supplied minimum check should pass after your change. Add an API-level test that checks content type, status, request count and matching request ID in logs. Also verify that a retained entry does not enable fallback for this category. Select relevant regression tests and explain why they are relevant.

**Keep:** the new tests, test output, a safe log excerpt and a 100–150 word decision record. Address retry safety, latency budget, outward status, breaker counting and the evidence. Another defensible production policy is possible, but this teaching contract is the acceptance target.

## If time is short

Use the working Exercise 5 checkpoint and complete the investigation. Do not replace this block with Redis or more tutor demonstration. A justified diagnosis plus one meaningful test is the minimum evidence; finish the remaining assertions in catch-up time.

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
