#!/usr/bin/env python3
""" basic authentication module """
from api.v1.auth.auth import Auth
from base64 import b64decode


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ decodes the value of a base64 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # encoded = base64_authorization_header.encode('utf-8')
            # decoded64 = b64decode(encoded)
            decoded64 = b64decode(base64_authorization_header)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ returns the user email and password """
        if decoded_base64_autgorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        email, passwd = decoded_base64_authorization_header.split(":")
        return (email, passwd)
