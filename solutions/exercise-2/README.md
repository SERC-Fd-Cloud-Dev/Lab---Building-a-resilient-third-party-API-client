# Possible solution — Exercise 2

Configure timeouts and bounded retries. This is a cumulative application checkpoint, including earlier completed stages. Compare behaviour and reasoning, not only matching syntax.

From the repository root:

```bash
python tools/checkpoint.py exercise-2 .work/exercise-2-reference
cd .work/exercise-2-reference
python -m pytest tests/baseline tests/verification/test_retry.py -q
python -m uvicorn app.main:app --port 8000
```

Choose a new destination each time. The helper will not overwrite a folder.

Three total attempts use 0.1 and 0.2 seconds of backoff. Permanent errors re-raise immediately. HTTPX phase limits and the supplied total deadline serve different purposes.