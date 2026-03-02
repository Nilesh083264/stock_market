import json
import os
from constants.constant import TOKEN_PATH



class TokenManager:
    TOKEN_PATH = TOKEN_PATH

    @classmethod
    def get_access_token(cls) -> str:
        if not os.path.exists(cls.TOKEN_PATH):
            raise FileNotFoundError("tokens.json not found")

        with open(cls.TOKEN_PATH, "r") as f:
            token = json.load(f)

        if not token:
            raise ValueError("Access token missing in tokens.json")


        return token


token_service = TokenManager()
token = token_service.get_access_token()
