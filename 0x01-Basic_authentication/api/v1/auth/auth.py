#!/usr/bin/env python3
''' Authentication module '''
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class that handles api authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''validated required authorization'''
        return False

    def authorization_header(self, request=None) -> str:
        '''handles authorization header'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''checks current user status'''
        return None
