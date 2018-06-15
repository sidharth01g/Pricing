from pricing.src.models.stores.store import Store
from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup
import re
import pricing
import hashlib
from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])


class Item(object):

    def __init__(self, name: str, url: str, _id: Optional[str] = None) -> None:
        self.name = name
        self.url = url
        self._id = hashlib.sha1((self.url + self.name).encode()).hexdigest() if _id is None else _id
        self.price = None

        self.store = Store.find_by_url(url=self.url)

    def __repr__(self) -> str:
        return '<Item "{}" with URL "{}">'.format(self.name, self.url)

    def load_price(self) -> float:
        # <span id="priceblock_ourprice" class="a-size-medium a-color-price">$349.00</span>
        logger.debug('Load price for {}'.format(self))
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(markup=content, features="html.parser")
        logger.debug('Search tag name "{}" with attributes {}'.format(self.store.tag_name, self.store.query))
        element = soup.find(name=self.store.tag_name, attrs=self.store.query)

        string_price = element.text.strip()

        # pattern = re.compile('([\d]+[\.]*[\d]*)')
        pattern = re.compile('(\d+.\d+)')

        match = pattern.search(string_price)

        price = match.group()

        if type(price) is str:
            price = price.replace(',', '')

        price = float(price)
        self.price = price
        logger.debug('Price for item "{}" at "{}" is {}'.format(self.name, self.url, self.price))
        return self.price

    def insert_into_database(self):
        pricing.db.insert(collection_name=pricing.configuration['collections']['items_collection'],
                          data=self.get_dict())

    @classmethod
    def find_one_by_id(cls, _id: str):
        result = pricing.db.find_one(collection_name=pricing.configuration['collections']['items_collection'],
                                     query={'_id': _id})
        result = cls.wrap(result) if result else result
        return result

    @classmethod
    def wrap(cls, item_dict: Dict) -> 'Item':
        return cls(**item_dict)

    def get_dict(self) -> Dict:
        return {
            'name': self.name,
            'url': self.url,
            '_id': self._id,
        }
