#!/usr/bin/env python3
""" Contains the authentication class """
from flask import requests
from typing import List, TypeVar


class Auth:
    """ Authenticaton class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns false """
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None
