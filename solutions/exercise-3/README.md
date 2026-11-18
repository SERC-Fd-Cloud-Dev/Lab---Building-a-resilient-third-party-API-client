# Possible solution — Exercise 3

Integrate a circuit-breaker package. This is a cumulative application checkpoint, including earlier completed stages. Compare behaviour and reasoning, not only matching syntax.

From the repository root:

```bash
python tools/checkpoint.py exercise-3 .work/exercise-3-reference
cd .work/exercise-3-reference
python -m pytest tests/baseline tests/verification/test_retry.py tests/verification/test_breaker.py -q
python -m uvicorn app.main:app --port 8000
```

Choose a new destination each time. The helper will not overwrite a folder.

Breaker outside retries counts logical operations. Two exhausted calls produce six attempts and open the breaker. The package resets its consecutive count on non-counted exceptions.