from pricing.src.models.items.item import Item
from pricing.src.models.users.user import User
from pricing.src.config import GlobalConfig
from typing import Union


class Alert(object):

    def __init__(self, item: Item, price_threshold: Union[float, int], user: User) -> None:
        self.item = item
        self.price_threshold = price_threshold
        self.user = user

    def __repr__(self):
        return '<Alert for item "{}" to user "{}" at a threshold of {}{}>'.format(
            self.item, self.user, GlobalConfig.currency, self.price_threshold)
