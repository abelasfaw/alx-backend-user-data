#!/usr/bin/env python3
'''Basic Authentication module'''
from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    '''Basic authentication class'''

    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        '''returns the Base64 part of the Authorization header'''

        if (authorization_header is None):
            return None
        elif (not isinstance(authorization_header, str)):
            return None
        elif (not authorization_header.startswith("Basic ")):
            return None

        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        '''returns the decoded value of a Base64 string
        base64_authorization_header'''

        if (base64_authorization_header is None):
            return None
        if (not isinstance(base64_authorization_header, str)):
            return None

        try:
            utf8_encoded = base64_authorization_header.encode('utf-8')
            decoded = b64decode(utf8_encoded).decode('utf-8')
        except BaseException:
            return None
        return decoded
