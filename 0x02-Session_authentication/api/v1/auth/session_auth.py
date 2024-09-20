#!/usr/bin/env python3
"""
Implimenting the Session authontication
"""
from api.v1.auth.auth import Auth
import base64
from flask import request, jsonify, make_response
from typing import TypeVar
from uuid import uuid4
from models.user import User
from api.v1.views import app_views
from os import getenv


class SessionAuth(Auth):
    """
    Implimenting the Session authontication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Hondle login using email and password"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or len(email) == 0:
        return jsonify({ "error": "email missing" }), 400
    if password is None or len(password) == 0:
        return jsonify({ "error": "password missing" }), 400
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({ "error": "no user found for this email" }), 404
    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        new_session = auth.create_session(user.id)
        response = make_response(user.to_json())
        cookie_name = getenv("SESSION_NAME")
        response.set_cookie(cookie_name, new_session)
        return response
    return jsonify({ "error": "wrong password" }), 401
