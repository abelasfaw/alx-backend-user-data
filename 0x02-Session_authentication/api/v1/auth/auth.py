#!/usr/bin/env python3
''' Authentication module '''
from flask import request
from typing import List, TypeVar
from os import getenv


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
        elif (self.match_wildcard(path, excluded_paths)):
            return False

        elif (not path.endswith('/')):
            return (not((path + '/') in excluded_paths))
        else:
            return True

    def match_wildcard(self, path: str, excluded_paths: List[str]) -> bool:
        '''checks for excluded paths ending with *'''
        for single_path in excluded_paths:
            if (single_path.endswith('*')):
                if (path.startswith(single_path[:-1])):
                    return True
        return False

    def authorization_header(self, request=None) -> str:
        '''handles authorization header'''
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''checks current user status'''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if (request is None):
            return None
        session_name = getenv('SESSION_NAME')
        if (session_name is None):
            return None
        session_id = request.cookies.get(session_name)
        return session_id
