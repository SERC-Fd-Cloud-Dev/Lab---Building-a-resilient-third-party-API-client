# Possible solution — Exercise 4

Apply cache-backed fallback. This is a cumulative application checkpoint, including earlier completed stages. Compare behaviour and reasoning, not only matching syntax.

From the repository root:

```bash
python tools/checkpoint.py exercise-4 .work/exercise-4-reference
cd .work/exercise-4-reference
python -m pytest tests/baseline tests/verification/test_retry.py tests/verification/test_breaker.py tests/verification/test_fallback.py -q
python -m uvicorn app.main:app --port 8000
```

Choose a new destination each time. The helper will not overwrite a folder.

Fresh data lasts under 10 seconds. Retained data is usable under 60 seconds only for eligible temporary failures. The breaker sees the failure before fallback returns success.