# Possible solution — Exercise 7

Investigate Redis caching. This is a cumulative application checkpoint, including earlier completed stages. Compare behaviour and reasoning, not only matching syntax.

From the repository root:

```bash
python tools/checkpoint.py exercise-7 .work/exercise-7-reference
cd .work/exercise-7-reference
python -m pytest tests/baseline tests/verification/test_retry.py tests/verification/test_breaker.py tests/verification/test_fallback.py tests/verification/test_logging.py tests/verification/test_independent.py tests/verification/test_redis.py -q
python -m uvicorn app.main:app --port 8000
```

Choose a new destination each time. The helper will not overwrite a folder.

Redis TTL follows retention, not freshness. Cache read failure becomes a miss; write failure does not fail a successful upstream response. Both dependencies failing yields a controlled error. The fake-client tests do not replace a real-container check.