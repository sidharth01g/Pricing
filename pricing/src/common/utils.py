from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    @staticmethod
    def encrypt_password(password_hashed: str) -> str:
        """
        Encrypts a hashed password string using pbkdf2_sha512
        Args:
            password_hashed: a hashed password

        Returns:
            A pbkdf2_sha512 encrypted version of the given hashed password
        """

        return pbkdf2_sha512.encrypt(password_hashed)

    @staticmethod
    def verify_password(password_hashed: str, password_encrypted: str) -> bool:
        """
        Takes in a hashed password and a pbkdf2_sha512 encrypted password and  validates the hashed password against the
        encrypted password.

        The hashed password is a hashed version of the password input by the user and the encrypted password is the one
        stored in the database

        Args:
            password_hashed: A hashed password supplied by the user during login attempt
            password_encrypted: A encrypted version of the password with which the user has signed up

        Returns:
            True if the password is validated, False otherwise
        """

        return pbkdf2_sha512.verify(password_hashed, password_encrypted)

    @staticmethod
    def is_valid_email(input_string: str) -> bool:
        """
        Uses a regular expression matcher to match valid email addresses

        Args:
            input_string: Email ID

        Returns:
            True if the input string is an email, else False
        """

        email_address_matcher = re.compile(pattern='^[\w-]+@([\w-]+.)+[\w]+$')

        return True if email_address_matcher.match(input_string) else False
