#!/usr/bin/env python3
"""
Authentication system, based on Session ID stored in database
"""
from models.base import Base


class UserSession(Base):
    """Store sessions in file to avoid loosing them when reload"""
    def __init__(self, *args: list, **kwargs: dict):
        """Init to declear sessions"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
