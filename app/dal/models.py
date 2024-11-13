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


if __name__ == '__main__':
    pass

