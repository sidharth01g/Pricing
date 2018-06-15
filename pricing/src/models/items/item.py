from typing import Dict
import requests
from bs4 import BeautifulSoup
import re
import pricing
import hashlib


class Item(object):

    def __init__(self, name: str, url: str, _id: str = None) -> None:
        self.name = name
        self.url = url
        self._id = hashlib.sha1((self.url + self.name).encode()).hexdigest() if _id is None else _id
        self.price = None

    def __repr__(self) -> str:
        return '<Item "{}" with URL "{}">'.format(self.name, self.url)

    def load_price(self, tag_name: str, query: dict) -> float:
        # <span id="priceblock_ourprice" class="a-size-medium a-color-price">$349.00</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(markup=content, features="html.parser")
        element = soup.find(name=tag_name, attrs=query)

        string_price = element.text.strip()

        # pattern = re.compile('([\d]+[\.]*[\d]*)')
        pattern = re.compile('(\d+.\d+)')

        match = pattern.search(string_price)

        price = match.group()

        if type(price) is str:
            price = price.replace(',', '')

        price = float(price)
        self.price = price
        return self.price

    def insert_into_database(self):
        pricing.db.insert(collection_name=pricing.configuration['collections']['items_collection'], data=self.__dict__)

    @classmethod
    def find_one_by_id(cls, _id: str):
        result = pricing.db.find_one(collection_name=pricing.configuration['collections']['items_collection'],
                                     query={'_id': _id})
        result = cls.wrap(result) if result else result
        return result

    @classmethod
    def wrap(cls, item_dict: Dict) -> 'Item':
        return cls(**item_dict)
