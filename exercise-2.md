# Exercise 2 — Configure timeouts and bounded retries

Implement a retry policy for read-only supplier requests and verify its limits.

**Time:** 40 minutes. **Work:** individual, compare reasoning with a partner after checking.


## Before you start

Work in `app/resilience.py`. `operation` is an async callable for one attempt. It raises `UpstreamFailure`; its `retryable` flag expresses the integration policy. The service already applies a two-second total operation deadline. HTTPX's connect, read, write and pool limits are phase/inactivity limits, not a complete response deadline.

## Guided walkthrough

Run `python -m pytest tests/verification/test_retry.py -q`. Several tests should fail before implementation. Read `test_transient_recovery`: its fake sleep records delays without making you wait.

Configure the supplied helper:

```python
def request_timeout():
    return httpx.Timeout(connect=0.5, read=0.5, write=0.5, pool=0.5)
```

Run `python tools/timeout_probe.py` to observe a real localhost read timeout. The simulator tests deliberately inject an exception instead.

## Guided application

Replace the single attempt inside `retry_call` with this control structure, completing the student-owned conditions:

```python
for attempt in range(1, 4):
    emit('upstream_attempt', attempt=attempt)
    try:
        return await operation()
    except UpstreamFailure as error:
        # Stop if this error is not retryable OR this was the last attempt.
        # Otherwise calculate delay, emit retry_scheduled and await sleep(delay).
        ...
```

Use **three total attempts**, backoff `0.1 * 2 ** (attempt - 1)` and no sleep after the final attempt. Re-raise the final exception with `raise`; do not silently return `None`. Use `await sleep(...)`, which supports fast deterministic tests. Emit the retry event with `attempt`, `delay` and `kind=error.kind`.

## Supported practice

Run the retry file again. Expect **8 passes**: flaky recovery uses two attempts and `[0.1]`; persistent failures use three attempts and `[0.1, 0.2]`; permanent failures use one attempt with no sleep.

## Required decision

Add one boundary test or parameter case and explain your choice. For example, check that an invalid 200 response does not become a retry merely because JSON parsing failed. Estimate the delay added by backoff, then explain why this estimate is not a measured network latency or an SLA guarantee.

**Success criteria:** bounded attempts, explicit HTTPX phase limits, final error propagated and passing targeted tests. Optional: describe how jitter would spread many clients' retries; keep deterministic delays in the core lab.

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
