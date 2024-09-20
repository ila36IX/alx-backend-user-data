#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv("AUTH_TYPE", None)
if auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    print("Hello world")
    auth = SessionExpAuth()
elif auth_type:
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def check_protected():
    """Check if path is open or raise error if it's protected"""
    if auth is None:
        return
    protected_urls = ["/api/v1/stat*", "/api/v1/auth_session/login/"]
    if auth.require_auth(request.path, protected_urls) is False:
        return
    if auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)
    if request.path in ["/api/v1/users/me", "/api/v1/users/me/"]:
        return


@app.errorhandler(401)
def not_auth(error) -> str:
    """Unauthorized resourse"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """forbidden resourse"""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
