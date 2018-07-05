from pricing.src.models.items.item import Item
from pricing.src.config import GlobalConfig
from typing import Union, List, Dict, Optional
import hashlib
import pricing
import requests
import datetime
from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])


class Alert(object):

    def __init__(self, item_id: str, price_threshold: Union[float, int], user_email: str,
                 last_checked_time: Optional[datetime.datetime] = None, _id: Optional[str] = None) -> None:
        # Assert that the item exists in the database
        self.item = Item.find_one_by_id(_id=item_id)
        assert self.item is not None

        # Assert that the user_email is a registered one (i.e present in the users collection)
        assert Alert.is_email_registered(user_email)

        # Parameters to be saved into database
        self.item_id = item_id
        self.price_threshold = price_threshold
        self.user_email = user_email
        self.last_checked_time = datetime.datetime.utcnow() if last_checked_time is None else last_checked_time
        self._id = hashlib.sha1(
            (str(self.user_email) + str(self.item_id)).encode('utf-8')).hexdigest() if _id is None else _id

    def __repr__(self) -> str:
        return '<Alert for item "{}" to user "{}" at a threshold of {}{}>'.format(
            self.item.name, self.user_email, GlobalConfig.currency, self.price_threshold)

    def send_alert_email(self) -> None:
        url = pricing.configuration['alert_settings']['url']
        data = {
            'from': pricing.configuration['alert_settings']['from'],
            'to': self.user_email,
            'subject': 'Price for {} is within your limit of ${}'.format(self.item.name, self.price_threshold),
            'text': 'Hi! Your item is now available at the price you quoted',
        }
        auth = ('api', pricing.configuration['alert_settings']['api_key'])

        logger.debug('Sending alert data:\n{}'.format(data))
        logger.debug('URL: {}'.format(url))

        requests.post(url=url, data=data, auth=auth)

    @classmethod
    def get_alerts_to_update(cls) -> List['Alert']:
        updation_interval_minutes = pricing.configuration['alert_settings']['updation_interval_minutes']
        cutoff_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=updation_interval_minutes)
        results = pricing.db.find(
            collection_name=pricing.configuration['collections']['alerts_collection'],
            query={'last_checked_time': {'$lte': cutoff_time}}
        )
        results = [Alert.wrap(result) for result in results] if results else results
        return results

    def get_dict(self) -> Dict:
        return {
            'item_id': self.item_id,
            'price_threshold': self.price_threshold,
            'user_email': self.user_email,
            'last_checked_time': self.last_checked_time,
            '_id': self._id,
        }

    @classmethod
    def wrap(cls, alert_dict: Dict) -> 'Alert':
        return cls(**alert_dict)

    @staticmethod
    def is_email_registered(email: str) -> bool:
        result = pricing.db.find_one(collection_name=pricing.configuration['collections']['users_collection'],
                                     query={'email': email})
        return result is not None

    def insert_into_database(self) -> None:
        pricing.db.insert(collection_name=pricing.configuration['collections']['alerts_collection'],
                          data=self.get_dict())

    def update_in_database(self) -> None:
        pricing.db.update(collection_name=pricing.configuration['collections']['alerts_collection'],
                          data=self.get_dict(), upsert=True)

    def fetch_item_price(self) -> float:
        logger.debug('Fetching price of {}'.format(self.item))
        assert self.item is not None
        self.item.load_price()
        self.last_checked_time = datetime.datetime.utcnow()
        self.update_in_database()
        return self.item.price

    def send_email_if_price_reached(self) -> None:
        logger.debug('Checking if {} reached threshold price'.format(self))
        current_price = self.fetch_item_price()
        logger.debug('Price of {} is {}'.format(self.item, current_price))
        if current_price <= self.price_threshold:
            logger.debug('Alert: {} reached threshold price of {}'.format(self, self.price_threshold))
            self.send_alert_email()

    @classmethod
    def find_by_email(cls, email: str) -> List['Alert']:
        results = pricing.db.find(collection_name=pricing.configuration['collections']['alerts_collection'],
                                  query={'user_email': email})
        results = [cls.wrap(result) for result in results] if results else results
        return results

    @classmethod
    def find_one_by_id(cls, _id: str) -> 'Alert':
        result = pricing.db.find_one(collection_name=pricing.configuration['collections']['alerts_collection'],
                                     query={'_id': _id})
        result = cls.wrap(result) if result else result
        return result
