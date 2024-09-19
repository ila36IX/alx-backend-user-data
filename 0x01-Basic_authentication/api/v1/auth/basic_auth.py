#!/usr/bin/env python3
"""
For the moment is empty
"""
from api.v1.auth.auth import Auth
import base64


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
