# Possible solution — Movie Guessing Game homework

This self-contained reference keeps TMDB communication in `movie_game/services/tmdb.py`. It adds bounded retries and safe JSON logs while retaining the original routes and authentication.

From the repository root:

```bash
python tools/checkpoint.py homework .work/homework-reference
cd .work/homework-reference
python -m pytest tests verification -q
python -m uvicorn movie_game.main:app --port 8001
```

Expected core result: 8 tests pass. The supplied extra solution test verifies a timeout followed by success and correct attempt count. GET retries are safe at the operation-semantics level but still consume quota. A 401 is a supplier-credential issue and should not be retried automatically. Upstream 429 produces a controlled 503 without immediate retry. The incoming game key is checked before the service runs and is never sent to TMDB.

Alternative implementations are acceptable when they meet the same contracts, attempt/delay limits and safe diagnostic behaviour. Keep service concerns out of route code.
