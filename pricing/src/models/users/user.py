import hashlib
import pricing
from pricing.src.common.utils import Utils
from typing import Dict
from pricing.src.common.logging_base import Logging
import pricing.src.models.users.errors as user_errors

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')


class User(object):

    def __init__(self, email: str, password_encrypted: str) -> None:
        self.email = email
        self.password_encrypted = password_encrypted
        self._id = hashlib.sha1(self.email.lower().encode()).hexdigest()

    def __repr__(self) -> str:
        return '<User with email ID "{}">'.format(self.email)

    @staticmethod
    def is_login_valid(email: str, password_hashed: str, configuration: Dict) -> bool:
        """
        Validates an email ID, password combination

        Args:
            email: Email ID
            password_hashed: A sha512 hashed password
            configuration: Config dict
        Returns:
            True if valid, False otherwise
        """

        collection_name = configuration['collections']['users_collection']
        query = {'email': email}
        result = pricing.db.find_one(collection_name=collection_name, query=query)

        if result is None:
            # TODO: tell the user that the email is not registered
            logger.debug('No results found for user "{}'.format(email))
            raise user_errors.UserNotExistsError(message='No user found matching {}'.format(email))
            # return False

        password_valid = Utils.verify_password(password_hashed=password_hashed,
                                               password_encrypted=result['password_hashed'])

        if password_valid is not True:
            # TODO: tell the user the password_hashed is not valid
            logger.debug('Password not valid for "{}'.format(email))
            raise user_errors.IncorrectPasswordError(message='Password validation failed')
            # return False

        return True

    @staticmethod
    def register_user(email: str, password_hashed: str) -> bool:
        """
        Register a new user using an email ID and a sha-512 hashed password_hashed

        Args:
            email: Email ID
            password_hashed: sha-512 hashed password_hashed of the user

        Returns:
            True if registration is successful, False otherwise
        """

        if Utils.is_valid_email(input_string=email) is not True:
            # Email ID is not a valid one
            raise user_errors.InvalidEmailError(message='Email ID "{}" is not valid'.format(email))

        result = pricing.db.find_one(collection_name=pricing.configuration['collections']['users_collection'],
                                     query={'email': email})

        if result is not None:
            # User is already registered
            raise user_errors.UserAlreadyRegisteredError(message='User {} is already registered'.format(email))

        user_new = User(email=email, password_encrypted=Utils.encrypt_password(password_hashed=password_hashed))
        user_new.insert_into_database()
        return True

    def insert_into_database(self):
        pricing.db.insert(collection_name=pricing.configuration['collections']['users_collection'], data=self.__dict__)

    @classmethod
    def wrap(cls, user_instance: 'User'):
        return cls(**user_instance)
