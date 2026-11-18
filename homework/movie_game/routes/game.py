import secrets
from fastapi import APIRouter, Request, Header, HTTPException, Depends
router = APIRouter()

def require_key(request: Request, x_api_key: str | None = Header(default=None)):
    expected = request.app.state.settings.game_api_key
    if not x_api_key or not secrets.compare_digest(x_api_key.encode(), expected.encode()):
        raise HTTPException(401, 'Valid game API key required')

@router.get('/games/{movie_id}/clue')
async def clue(movie_id: int, request: Request):
    movie = await request.app.state.tmdb.movie(movie_id, request.state.request_id)
    return {'movie_id':movie.id, 'year':movie.release_date[:4], 'runtime_minutes':movie.runtime}

@router.get('/games/{movie_id}/answer', dependencies=[Depends(require_key)])
async def answer(movie_id: int, request: Request):
    movie = await request.app.state.tmdb.movie(movie_id, request.state.request_id)
    return {'movie_id':movie.id, 'title':movie.title}
