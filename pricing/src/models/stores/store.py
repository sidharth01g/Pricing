from typing import Dict, Optional, List
import hashlib
import pricing
import pricing.src.models.stores.errors as store_errors
from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])


class Store(object):

    def __init__(self, name: str, url_prefix: str, tag_name: str, query: Dict, _id: Optional[str] = None) -> None:
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = hashlib.sha1((self.url_prefix + self.name + self.tag_name + str(
            self.query)).encode()).hexdigest() if _id is None else _id

    def __repr__(self) -> str:
        return '<Store "{}" with URL prefix "{}">'.format(self.name, self.url_prefix)

    def get_dict(self) -> Dict:
        return {
            'name': self.name,
            'url_prefix': self.url_prefix,
            'tag_name': self.tag_name,
            'query': self.query,
            '_id': self._id,
        }

    def insert_into_database(self):
        pricing.db.insert(collection_name=pricing.configuration['collections']['stores_collection'],
                          data=self.get_dict())

    @classmethod
    def wrap(cls, store_dict: Dict) -> 'Store':
        return cls(**store_dict)

    @classmethod
    def find_one_by_id(cls, _id: str) -> Optional['Store']:
        result = pricing.db.find(collection_name=pricing.configuration['collections']['stores_collection'],
                                 query={'_id': _id})
        return cls.wrap(store_dict=result)

    @classmethod
    def find_by_name(cls, name: str) -> List['Store']:
        results = pricing.db.find(collection_name=pricing.configuration['collections']['stores_collection'],
                                  query={'name': name})

        results = [cls.wrap(store_dict=result) for result in results]
        return results

    @classmethod
    def find_one_by_name(cls, name: str) -> Optional['Store']:
        result = pricing.db.find_one(collection_name=pricing.configuration['collections']['stores_collection'],
                                     query={'name': name})
        result = cls.wrap(store_dict=result)
        return result

    @classmethod
    def find_by_url_prefix(cls, url_prefix: str) -> Optional['Store']:
        results = pricing.db.find(collection_name=pricing.configuration['collections']['stores_collection'],
                                  query={'url_prefix': {'$regex': '^{}'.format(url_prefix)}})

        results = [cls.wrap(store_dict=result) for result in results] if results else results
        return results

    @classmethod
    def find_one_by_url_prefix(cls, url_prefix: str) -> Optional['Store']:
        result = pricing.db.find_one(collection_name=pricing.configuration['collections']['stores_collection'],
                                     query={'url_prefix': {'$regex': '^{}'.format(url_prefix)}})

        result = cls.wrap(store_dict=result) if result else result
        return result

    @classmethod
    def find_by_url(cls, url: str) -> Optional['Store']:
        for i in range(len(url), 0, -1):
            result = Store.find_one_by_url_prefix(url_prefix=url[:i])
            if result:
                logger.debug('Found a match {} for url {}'.format(result, url))
                return result
        raise store_errors.StoreNotFoundError(message='No store found matching URL "{}"'.format(url))

    @classmethod
    def get_all_stores(cls):
        results = pricing.db.find(collection_name=pricing.configuration['collections']['stores_collection'], query={})
        results = [cls.wrap(store_dict=result) for result in results] if results else results
        return results
