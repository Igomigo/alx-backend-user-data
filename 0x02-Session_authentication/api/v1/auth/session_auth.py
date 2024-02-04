#!/usr/bin/env python3
""" contains the session auth class
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ The Session auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates the session ID for a user """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id: str = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns user id based on session id """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id: str = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ Returns user instance based on the cookie
            value received
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ deletes the user session/logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
