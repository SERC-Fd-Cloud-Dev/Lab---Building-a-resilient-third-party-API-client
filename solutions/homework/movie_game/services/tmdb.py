import asyncio
import logging
import json
import httpx
from pydantic import BaseModel, Field, ValidationError

class Movie(BaseModel):
    id: int
    title: str
    release_date: str
    runtime: int = Field(gt=0)

class TMDBFailure(Exception):
    def __init__(self, kind, status=502, retryable=False):
        self.kind, self.status, self.retryable = kind, status, retryable
        super().__init__(kind)

class TMDBService:
    def __init__(self, client, *, sleep=asyncio.sleep):
        self.client, self.sleep = client, sleep

    async def _once(self, movie_id):
        try:
            r = await self.client.get(f'/3/movie/{movie_id}')
        except httpx.TimeoutException:
            raise TMDBFailure('timeout',504,True) from None
        except httpx.TransportError:
            raise TMDBFailure('connection',503,True) from None
        if r.status_code in {500,502,503,504}:
            raise TMDBFailure('unavailable',503,True)
        if r.status_code == 429:
            raise TMDBFailure('rate_limited',503)
        if r.status_code == 404:
            raise TMDBFailure('missing',404)
        if r.status_code != 200:
            raise TMDBFailure('rejected',502)
        try:
            movie = Movie.model_validate(r.json())
            if movie.id != movie_id:
                raise ValueError('mismatched movie')
            return movie
        except (ValueError, ValidationError):
            raise TMDBFailure('invalid_response',502) from None

    async def movie(self, movie_id, request_id):
        logger = logging.getLogger('movie_game')
        for attempt in range(1, 4):
            logger.info(json.dumps({'event':'tmdb_attempt','request_id':request_id,'attempt':attempt}))
            try:
                result = await self._once(movie_id)
            except TMDBFailure as error:
                if not error.retryable or attempt == 3:
                    logger.warning(json.dumps({'event':'tmdb_failed','request_id':request_id,'kind':error.kind}))
                    raise
                delay = 0.1 * 2 ** (attempt - 1)
                logger.warning(json.dumps({'event':'tmdb_retry','request_id':request_id,
                                           'attempt':attempt,'delay':delay}))
                await self.sleep(delay)
            else:
                logger.info(json.dumps({'event':'tmdb_success','request_id':request_id,'attempt':attempt}))
                return result
