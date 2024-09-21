#!/usr/bin/env python3
"""
Authentication system, based on Session ID stored in database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """Authentication system, based on Session ID stored in database"""
    def create_session(self, user_id=None):
        """Testing is everything """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        UserSession.load_from_file()
        if type(session_id) is not str:
            return None
        session_dict = UserSession.search({"session_id": session_id})
        if len(session_dict) == 0:
            return None
        session = session_dict[0]
        delta_time = datetime.now() - session.created_at
        if delta_time.total_seconds() > self.session_duration:
            session.remove()
            return None
        return session_dict[0].user_id

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        session_id = self.session_cookie(request)
        UserSession.load_from_file()
        if session_id is None:
            return False
        session_dict = UserSession.search({"session_id": session_id})
        if len(session_dict) == 0:
            return False
        user_id = getattr(session_dict[0], "user_id")
        if user_id is None:
           return False
        session_dict[0].remove()
        return True
