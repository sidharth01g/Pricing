from typing import Union


class Item(object):

    def __init__(self, name: str, url: str, price: Union[float, int]) -> None:
        self.name = name
        self.url = url
        self.price = price

    def __repr__(self) -> str:
        return '<Item "{}" with URL "{}">'.format(self.name, self.url)
