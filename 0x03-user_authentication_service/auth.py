#!/usr/bin/env python3
""" Contains the authentication systems
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


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

    def register_user(self, email: str, passwd: str) -> User:
        """ Registers user to the database """
        if email is None or passwd is None:
            return None

        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_passwd = _hash_password(passwd)
        user = self._db.add_user(email, hashed_passwd)
        return user
