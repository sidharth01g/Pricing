from pricing.src.models.items.item import Item
from pricing.src.config import GlobalConfig
from typing import Union, List, Dict, Optional
import hashlib
import pricing
import requests
import datetime


class Alert(object):

    def __init__(self, item_id: str, price_threshold: Union[float, int], user_email: str,
                 last_checked_time: datetime.datetime, _id: Optional[str] = None) -> None:
        # Assert that the item exists in the database
        self.item = Item.find_one_by_id(_id=self.item_id)
        assert self.item is not None

        # Assert that the user_email is a registered one (i.e present in the users collection)
        assert Alert.is_email_registered(user_email)

        # Parameters to be saved into database
        self.item_id = item_id
        self.price_threshold = price_threshold
        self.user_email = user_email
        self.last_checked_time = datetime.datetime.utcnow() if last_checked_time is None else last_checked_time
        self._id = hashlib.sha1(str(self.user_email) + str(self.item_id)).hexdigest() if _id is None else _id

    def __repr__(self) -> str:
        return '<Alert for item "{}" to user "{}" at a threshold of {}{}>'.format(
            self.item.name, self.user_email, GlobalConfig.currency, self.price_threshold)

    def send_alert_email(self) -> None:
        requests.post(
            url=pricing.configuration['alert_settings']['url'],
            data={
                'from': pricing.configuration['alert_settings']['from'],
                'to': self.user_email,
                'subject': 'Price for {} is within your limit of ${}'.format(self.item.name, self.price_threshold),
                'text': None,
            },
            auth=pricing.configuration['alert_settings']['api_key']

        )

    @classmethod
    def get_alerts_to_update(cls) -> List['Alert']:
        updation_interval_minutes = pricing.configuration['alert_settings']['updation_interval_minutes']
        cutoff_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=updation_interval_minutes)
        results = pricing.db.find(
            collection_name=pricing.configuration['collections']['alerts_collection'],
            query={'last_checked_time': {'$lte': cutoff_time}}
        )
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
