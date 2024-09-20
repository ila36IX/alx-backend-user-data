#!/usr/bin/env python3
"""
Adding the expiration to the Session authontication
"""
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """Adding the expiration to the Session authontication"""
    
    def __init__(self):
        """Overloading the init method"""
        session_duration = getenv("SESSION_DURATION", 0)

    def create_session(self, user_id=None):
        """Create the session and assign an expiration date to it"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gete the user from the session poll"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        if "created_at" not in self.user_id_by_session_id:
            return None
        delta_time = datatime.now() - session_dict["created_at"]
        if delta_time.total_seconds() > self.session_duration:
            return None
            return session_dict.get("user_id")
