
from pydantic_mongo import AbstractRepository, PydanticObjectId

from dal.models import AppModel, LogModel

class AppRepository(AbstractRepository[AppModel]):
    class Meta:
        collection_name = "apps"

class LoggerRepository(AbstractRepository[LogModel]):
    class Meta:
        collection_name = "logs"


if __name__ == '__main__':
    import os
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    # todo test the repository
    client = MongoClient(os.environ.get("MONGODB_CONNSTR") , server_api=ServerApi('1'))
    db = client.get_database("chatapp")
    app_repo = AppRepository(database=db)
    app = AppModel()
    app_repo.save(app)