import httpx
from fastapi.testclient import TestClient
from movie_game.main import create_app
from movie_game.config import Settings

def test_offline_clue_does_not_leak_title():
    with TestClient(create_app()) as c:
        result=c.get('/games/11/clue')
        assert result.status_code==200
        assert result.json()=={'movie_id':11,'year':'2001','runtime_minutes':112}

def test_protection_before_tmdb_request():
    calls=[]
    def handle(request):
        calls.append(request)
        return httpx.Response(200,json={'id':11,'title':'Example','release_date':'2001-01-01','runtime':112})
    with TestClient(create_app(Settings(game_api_key='test-key'),httpx.MockTransport(handle))) as c:
        assert c.get('/games/11/answer').status_code==401
        assert c.get('/games/11/answer',headers={'X-API-Key':'wrong'}).status_code==401
        assert len(calls)==0
        assert c.get('/games/11/answer',headers={'X-API-Key':'test-key'}).json()['title']=='Example'
        assert len(calls)==1
