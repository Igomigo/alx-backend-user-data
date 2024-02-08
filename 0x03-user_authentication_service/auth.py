#!/usr/bin/env python3
""" Contains the authentication systems
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ Method hashes a password """
    if password is None:
        return None
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user in the database
        Returns: User Object
        """

        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

    def valid_login(self, email: str, pwd: str) -> bool:
        """ provides the mechanism for logging in a user """
        if email is None or pwd is None:
            return None
        pwd = pwd.encode('utf-8')
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(pwd, user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False
