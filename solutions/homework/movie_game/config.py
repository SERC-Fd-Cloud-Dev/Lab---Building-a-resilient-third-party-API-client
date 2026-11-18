import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

@dataclass
class Settings:
    tmdb_token: str = ''
    game_api_key: str = 'local-practice-only'
    offline: bool = True

    @classmethod
    def from_env(cls):
        return cls(os.getenv('TMDB_READ_TOKEN',''),
                   os.getenv('GAME_API_KEY','local-practice-only'),
                   os.getenv('TMDB_MODE','offline') != 'live')
