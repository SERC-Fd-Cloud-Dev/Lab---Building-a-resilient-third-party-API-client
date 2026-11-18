# Possible solution — Exercise 6

Investigate a rate-limited dependency. This is a cumulative application checkpoint, including earlier completed stages. Compare behaviour and reasoning, not only matching syntax.

From the repository root:

```bash
python tools/checkpoint.py exercise-6 .work/exercise-6-reference
cd .work/exercise-6-reference
python -m pytest tests/baseline tests/verification/test_retry.py tests/verification/test_breaker.py tests/verification/test_fallback.py tests/verification/test_logging.py tests/verification/test_independent.py -q
python -m uvicorn app.main:app --port 8000
```

Choose a new destination each time. The helper will not overwrite a folder.

429 is not retried within a two-second interactive budget when the supplier requests 20 seconds. API 503 describes this shared dependency limit. The breaker excludes this deliberate quota policy. See test_independent_extra.py for an additional API/log test. A production queue might schedule a later safe read with a validated retry window.