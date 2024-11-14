from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, PydanticObjectId
from pymongo import MongoClient
from typing import Optional, List


CHAT_DEFAULT_TEXT = "Ask me something."
SEARCH_DEFAULT_TEXT = "Search for something."
SYSTEM_PROMPT_DEFAULT = "You are a Helpful AI Assistant"


class AppModel(BaseModel):
    id: str = ObjectId().__str__()
    created: str = datetime.now().isoformat()
    title: str = ""
    caption: str = ""
    system_prompt: str = SYSTEM_PROMPT_DEFAULT
    search_placeholder: str = SEARCH_DEFAULT_TEXT
    chat_placeholder: str = CHAT_DEFAULT_TEXT
    temperature: Optional[float] = 0.7
    chat_mode_querystring: str = f"?appid={id}&mode=chat&userid=SOMEUSER"
    search_mode_querystring: str = f"?appid={id}&mode=search&userid=SOMEUSER"
    auth_email: str = ""
    

class AuthModel(BaseModel):
    session_id: str = ""
    email: str = ""
    name: str = ""
    auth_data: dict = {}

    @staticmethod
    def from_auth_data(auth_data: dict):
        return AuthModel(session_id=auth_data["account"]["localAccountId"],
                              email=auth_data['account']["idTokenClaims"]["preferred_username"],
                              name=auth_data['account']["idTokenClaims"]["name"],
                              auth_data=auth_data)

class LogModel(BaseModel):
    id: str = ObjectId().__str__()
    appid: str = ""
    userid: str = ""
    timestamp: str = datetime.now().isoformat()
    mode: str = "" # "chat" or "search"
    role: str = "" # "user", "system", or "assistant"
    content: str = ""


if __name__ == '__main__':
    a = AuthModel.from_auth_data(auth_data={"account": {"localAccountId": "123", "idTokenClaims": {"preferred_username": "bob@bob", "name": "Bob"}}})
    print(a)
