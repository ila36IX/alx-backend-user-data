#!/usr/bin/env python3
"""
For the moment is empty
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """
    For the moment is empty
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header for a Basic
        Authentication"""
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith("Basic "):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """returns the decoded value of a Base64 string"""
        if type(base64_authorization_header) is not str:
            return None
        try:
            auth_header = base64.b64decode(base64_authorization_header)
            return auth_header.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self, 
                                     user_email: str, 
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if user_email is None or user_pwd is None:
            return None
        from models.user import User
        attrubutes = {"email": user_email}
        users = User.search()
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None


