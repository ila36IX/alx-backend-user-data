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
        print(tuple(decoded_base64_authorization_header.split(':', 1)))
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        from models.user import User
        attrubutes = {"email": user_email}
        users = User.search()
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        auth_base64 = self.extract_base64_authorization_header(auth_header)
        auth_str = self.decode_base64_authorization_header(auth_base64)
        email, password = self.extract_user_credentials(auth_str)
        user = self.user_object_from_credentials(email, password)
        return user
