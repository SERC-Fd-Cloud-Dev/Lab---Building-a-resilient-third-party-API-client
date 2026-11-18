# Possible solution — Exercise 5

Record structured diagnostic events. This is a cumulative application checkpoint, including earlier completed stages. Compare behaviour and reasoning, not only matching syntax.

From the repository root:

```bash
python tools/checkpoint.py exercise-5 .work/exercise-5-reference
cd .work/exercise-5-reference
python -m pytest tests/baseline tests/verification/test_retry.py tests/verification/test_breaker.py tests/verification/test_fallback.py tests/verification/test_logging.py -q
python -m uvicorn app.main:app --port 8000
```

Choose a new destination each time. The helper will not overwrite a folder.

Allowlisted JSON fields provide a request trace. Event-level severity makes retry/fallback visible without treating every recovered request as ERROR.