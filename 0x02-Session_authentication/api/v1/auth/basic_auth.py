#!/usr/bin/env python3
'''Basic Authentication module'''
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


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

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        '''returns the user email and password from the
        Base64 decoded value'''

        if (decoded_base64_authorization_header is None):
            return None, None
        if (not isinstance(decoded_base64_authorization_header, str)):
            return None, None
        if (not (':' in decoded_base64_authorization_header)):
            return None, None

        header = decoded_base64_authorization_header.split(':', 1)
        return header[0], header[1]

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        '''returns the User instance based on his email and password'''

        if (user_email is None or user_pwd is None):
            return None
        if (not isinstance(user_email, str) or not isinstance(user_pwd, str)):
            return None

        try:
            users = User.search({'email': user_email})
            for user in users:
                if (user.is_valid_password(user_pwd)):
                    return user

        except Exception:
            return None

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''overloads Auth and retrieves the User instance for a request'''
        header = self.authorization_header(request)
        if header is None:
            return None

        encoded_header = self.extract_base64_authorization_header(header)
        if encoded_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(
                            encoded_header)
        if decoded_header is None:
            return None

        email, password = self.extract_user_credentials(decoded_header)
        if email is None or password is None:
            return None

        user = self.user_object_from_credentials(email, password)
        return user
