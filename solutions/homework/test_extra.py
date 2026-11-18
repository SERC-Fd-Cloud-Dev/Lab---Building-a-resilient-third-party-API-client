import httpx
from movie_game.services.tmdb import TMDBService

async def test_timeout_then_success():
    calls=[]
    def handle(request):
        calls.append(request)
        if len(calls)==1: raise httpx.ReadTimeout('synthetic',request=request)
        return httpx.Response(200,json={'id':11,'title':'Example','release_date':'2001-01-01','runtime':112})
    async def sleep(_): pass
    async with httpx.AsyncClient(base_url='https://api.themoviedb.org',transport=httpx.MockTransport(handle)) as c:
        assert (await TMDBService(c,sleep=sleep).movie(11,'extra')).id==11
    assert len(calls)==2
