# Possible solution — Exercise 1

Observe and classify failures. This is a cumulative application checkpoint, including earlier completed stages. Compare behaviour and reasoning, not only matching syntax.

From the repository root:

```bash
python tools/checkpoint.py exercise-1 .work/exercise-1-reference
cd .work/exercise-1-reference
python -m pytest tests/baseline -q
python -m uvicorn app.main:app --port 8000
```

Choose a new destination each time. The helper will not overwrite a folder.

Baseline: flaky gives one 503 attempt; cache hits suppress calls. Payment retries need a separate idempotency guarantee.

## Example observation table

Reset before each independent scenario. Each starter call makes one supplier attempt.

| Scenario | Outward result | Meaning |
|---|---|---|
| timeout | 504 Problem Details | The dependency did not return within the simulated timeout |
| connection | 503 Problem Details | The dependency could not be reached |
| unavailable | 503 Problem Details | A temporary supplier response is translated |
| invalid | 502 Problem Details | HTTP success did not contain valid product data |
| unauthorised | 502 Problem Details | The supplier rejected the application's credential; this is not caller authentication |
| flaky | 503 on the first starter call | The starter does not retry; a later safe read could succeed |

After a successful seed, a second fresh read returns `source: cache` and leaves the supplier count at one. The GET can normally be repeated safely, but retries still consume time and quota. A payment timeout may hide a completed charge; use a verified idempotency guarantee or query the outcome before repeating the operation.
