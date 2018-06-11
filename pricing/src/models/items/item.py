from typing import Dict
from pricing.src.models.stores.store import Store
import requests
from bs4 import BeautifulSoup
import re
import pricing


class Item(object):

    def __init__(self, name: str, url: str, store: Store) -> None:
        self.name = name
        self.url = url
        self.store = store

        tag_name = store.tag_name
        query = store.query
        self.price = self.load_price(tag_name=tag_name, query=query)

    def __repr__(self) -> str:
        return '<Item "{}" with URL "{}">'.format(self.name, self.url)

    def load_price(self, tag_name: str, query: dict) -> float:
        # <span id="priceblock_ourprice" class="a-size-medium a-color-price">$349.00</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(markup=content, features="html.parser")
        element = soup.find(name=tag_name, attrs=query)

        string_price = element.text.strip()

        pattern = re.compile('([\d]+[.]*[\d]*)')
        match = pattern.search(string_price)

        price = match.group()

        return float(price)

    def insert_into_database(self):
        pricing.db.insert(collection_name=pricing.configuration['collections']['items_collection'], data=self.__dict__)

    @classmethod
    def wrap(cls, item_instance: Dict) -> 'Item':
        return cls(**item_instance)
