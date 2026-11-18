import json
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from http import HTTPStatus
from uuid import uuid4
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .config import Settings
from .services.tmdb import TMDBService, TMDBFailure
from .routes.game import router

logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)

def create_app(settings=None, transport=None, sleep=None):
    settings = settings or Settings.from_env()
    if not settings.offline and not settings.tmdb_token:
        raise RuntimeError('Set TMDB_READ_TOKEN for live mode or use offline mode.')
    if not settings.game_api_key:
        raise RuntimeError('GAME_API_KEY must not be empty.')

    def offline(request):
        fixture = Path(__file__).parents[1]/'fixtures/movie.json'
        data = json.loads(fixture.read_text())
        if request.url.path != '/3/movie/11':
            return httpx.Response(404)
        return httpx.Response(200,json=data)

    @asynccontextmanager
    async def lifespan(api):
        chosen = transport or (httpx.MockTransport(offline) if settings.offline else None)
        headers = {'Authorization':'Bearer '+settings.tmdb_token} if not settings.offline else {}
        async with httpx.AsyncClient(base_url='https://api.themoviedb.org',
                timeout=httpx.Timeout(0.5), transport=chosen, headers=headers) as client:
            api.state.tmdb = TMDBService(client, **({'sleep':sleep} if sleep else {}))
            yield

    api=FastAPI(title='Movie Guessing Game',lifespan=lifespan)
    api.state.settings=settings
    api.include_router(router)

    @api.middleware('http')
    async def correlation(request, call_next):
        request.state.request_id=str(uuid4())
        response=await call_next(request)
        response.headers['X-Request-ID']=request.state.request_id
        return response

    @api.exception_handler(TMDBFailure)
    async def upstream_error(request:Request,error:TMDBFailure):
        return JSONResponse(status_code=error.status,media_type='application/problem+json',
            content={'type':'about:blank','title':HTTPStatus(error.status).phrase,
                'status':error.status,'detail':'Movie information could not be retrieved.',
                'instance':'urn:uuid:'+request.state.request_id})
    return api

app=create_app()
