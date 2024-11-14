from datetime import datetime
from bson import ObjectId

from dal.repos import LoggerRepository
from dal.models import LogModel

class ChatLogger:

    def __init__(self, db):
        self.__db = db
        self.__repo = LoggerRepository(database=db)

    def log(self, appid, userid, timestamp, mode, role, content):
        lm = LogModel(id = ObjectId().__str__(),
                      appid=appid, 
                      userid=userid, 
                      timestamp=timestamp, 
                      mode=mode, 
                      role=role, 
                      content=content)
        return self.__repo.save(lm)
    
    def log_user_chat(self, appid, userid, prompt):
        return self.log(appid, userid, timestamp(), "chat", "user", prompt)
       
    def log_assistant_chat(self, appid, userid, response):
        return self.log(appid, userid, timestamp(), "chat", "assistant", response)
    
    def log_user_search(self, appid, userid, query):
        return self.log(appid, userid, timestamp(), "search", "user", query)
    
    def log_assistant_search(self, appid, userid, response):
        return self.log(appid, userid, timestamp(), "search", "assistant", response)

    def log_system_prompt(self, appid, userid, system_prompt):
        return self.log(appid, userid, timestamp(), "system", "system", system_prompt)


def timestamp(as_int=False):
    if not as_int:
        return datetime.now().isoformat()
    else:
        return int(datetime.now().timestamp())



    
