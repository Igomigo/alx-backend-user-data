#!/usr/bin/env python3
""" Contains the authentication class """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authenticaton class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ defining which routes to authenticate """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        path_len = len(path)
        if path_len == 0:
            return True
        hasSlash = True if path[path_len - 1] == "/" else False

        tmp_path = path
        if not hasSlash:
            tmp_path += "/"

        for i in excluded_paths:
            if tmp_path == i:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ validates all requests """
        if request is None or "Authorization" not in request.headers.keys():
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None
