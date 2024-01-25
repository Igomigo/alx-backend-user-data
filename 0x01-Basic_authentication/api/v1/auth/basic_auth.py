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

    def decode_base64_authorization_header\
            (self, base64_authorization_header: str) -> str:
        """ decodes the value of a base64 string """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded
