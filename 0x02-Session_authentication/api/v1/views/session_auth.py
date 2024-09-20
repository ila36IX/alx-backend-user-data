#!/usr/bin/env python3
"""
Implimenting the Session authontication routes
"""
from flask import request, jsonify, make_response
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Hondle login using email and password"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        new_session = auth.create_session(user.id)
        response = make_response(jsonify(user.to_json()))
        cookie_name = getenv("SESSION_NAME")
        response.set_cookie(cookie_name, new_session)
        return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """Route to hondle the logout by deleting the session id from sessions
    poll
    """
    from api.v1.app import auth
    session_deleted = auth.destroy_session(request)
    if not session_deleted:
        abort(404)
    return jsonify({}), 200
