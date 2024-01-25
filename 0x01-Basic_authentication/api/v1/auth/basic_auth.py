#!/usr/bin/env python3
""" basic authentication module """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ The basic auth class that inherits from the Auth class """
    
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the authentication value after Basic """
        if authorization_header is None or\
            not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]
