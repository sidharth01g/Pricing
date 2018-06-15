from typing import Dict
from pricing.src.models.stores.store import Store
import requests
from bs4 import BeautifulSoup
import re
import pricing
import hashlib


class Item(object):

    def __init__(self, name: str, url: str, _id: str = None) -> None:
        self.name = name
        self.url = url
        self.store = Store.find_by_url(url=self.url)
        self._id = hashlib.sha1((self.url + self.name).encode()).hexdigest() if _id is None else _id
        self.price = self.load_price()

    def __repr__(self) -> str:
        return '<Item "{}" with URL "{}">'.format(self.name, self.url)

    def load_price(self) -> float:
        # <span id="priceblock_ourprice" class="a-size-medium a-color-price">$349.00</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(markup=content, features="html.parser")
        element = soup.find(name=self.store.tag_name, attrs=self.store.query)

        string_price = element.text.strip()

        # pattern = re.compile('([\d]+[\.]*[\d]*)')
        pattern = re.compile('(\d+.\d+)')

        match = pattern.search(string_price)

        price = match.group()

        if type(price) is str:
            price = price.replace(',', '')

        return float(price)

    def insert_into_database(self):
        pricing.db.insert(collection_name=pricing.configuration['collections']['items_collection'], data=self.__dict__)

    @classmethod
    def wrap(cls, item_dict: Dict) -> 'Item':
        return cls(**item_dict)
