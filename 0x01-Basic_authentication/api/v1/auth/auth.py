#!/usr/bin/env python3
''' Authentication module '''
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class that handles api authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''identifies routes that need authentication'''
        if (path is None or excluded_paths is None):
            return True
        elif (len(excluded_paths) == 0):
            return True
        if (path in excluded_paths):
            return False
        elif (not path.endswith('/')):
            option2 = path + '/'
            return (not(option2 in excluded_paths))
        else:
            return True

    def authorization_header(self, request=None) -> str:
        '''handles authorization header'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''checks current user status'''
        return None
