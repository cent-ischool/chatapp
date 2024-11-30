from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, PydanticObjectId
from pymongo import MongoClient
from typing import Optional, List


PLACEHOLDER_TEXT = "Type something."
SEARCH_DEFAULT_TEXT = "Search for something."
SYSTEM_PROMPT_DEFAULT = "You are a Helpful AI Assistant"


class AppModel(BaseModel):
    # metadata
    id: str = ObjectId().__str__()
    auth_email: str = ""
    created: str = datetime.now().isoformat()
    mode: str = "chat" # "chat" or "search"

    # ui
    title: str = ""
    caption: str = ""
    user_avatar: str = "👤"
    assistant_avatar: str = "🤖"
    placeholder: str = PLACEHOLDER_TEXT

    # ai
    system_prompt: str = SYSTEM_PROMPT_DEFAULT
    temperature: Optional[float] = 0.7
    welcome_message: str = ""


    def build_querystring(self):
        querystring = f"?appid={self.id}&mode={self.mode}&userid=SOMEUSER"
        return querystring

    
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
