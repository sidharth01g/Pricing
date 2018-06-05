import pymongo
from typing import List, Dict
from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')


class Database(object):
    """
    The database class that abstracts Mongo DB operations
    """

    def __init__(self, db_name: str, uri: str = 'mongodb://127.0.0.0:27017') -> None:
        self.db_name = db_name
        self.uri = uri
        self.client = pymongo.MongoClient(self.uri)
        self.database = self.client[self.db_name]
        logger.debug('Create DB instance: {}'.format(self))

    def __repr__(self) -> str:
        return '<Database (MongoDB): URI: {}, database: {}>'.format(self.uri, self.database)

    def insert(self, collection_name: str, data: Dict) -> None:
        try:
            self.database[collection_name].insert(data)
        except Exception as e:
            logger.exception(e)
            raise e

    def find(self, collection_name: str, query: Dict) -> List[Dict]:
        assert type(query) is dict
        try:
            results = self.database[collection_name].find(query)
        except Exception as e:
            logger.exception(e)
            raise e
        return results

    def find_one(self, collection_name: str, query: Dict) -> Dict:
        assert type(query) is dict
        try:
            result = self.database[collection_name].find_one(query)
        except Exception as e:
            logger.exception(e)
            raise e
        return result
