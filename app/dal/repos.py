
from pydantic_mongo import AbstractRepository, PydanticObjectId

from models import AppModel

class AppRepository(AbstractRepository[AppModel]):
    class Meta:
        collection_name = "apps"


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