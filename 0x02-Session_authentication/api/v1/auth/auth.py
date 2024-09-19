#!/usr/bin/env python3
"""

Manage the API authentication.

"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return False if path doesn't requare auth, and True if the path
        is protected
            @excluded_paths: The paths that requered auth
        """
        if path is not None and len(path) > 1:
            if path[-1] != "/" and path[-1] != '*':
                path += "/"
        if excluded_paths is None:
            return True
        for open_path in excluded_paths:
            if open_path[-1] == "*":
                if path.startswith(open_path[:-1]):
                    return False
            if open_path == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the credintiols used by the user to authonticate"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Docs will ve added later after understanding what the function do"""
        return None
