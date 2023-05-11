#!/usr/bin/env python3
''' Authentication Module '''

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> str:
    '''takes password string and returns salted hash'''
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return password_hash


def _generate_uuid() -> str:
    '''Returns a string representation of a new UUID'''
    return str(uuid4())


class Auth:
    '''Authentication class'''

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''checks for existing user with input email and creates and
        saves user with hashed password'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        '''locates user by email and checks if password matches'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        encoded_password = password.encode()
        if bcrypt.checkpw(encoded_password, user_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        '''locates user by email, generates new uuid as session id and
        returns it'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        '''takes session_id input and returns corresponding user or none'''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        '''Updates the corresponding user's session ID to None'''
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        '''locates user by email, generates uuid and updates
        users reset_token'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''uses reset token to locate user and updates password'''
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
