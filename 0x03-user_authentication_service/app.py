#!/usr/bin/env python3
"""
Route module for the application
"""
from flask import Flask, jsonify, abort, request, make_response, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """the home endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register():
    """expected an email and password endpoint"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """create a new session for the user, store it the cookie with key
    `session_id` on the response and return a JSON payload of the form
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_user = AUTH.valid_login(email, password)
    if not valid_user:
        abort(401)
    session_id = AUTH.create_session(email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Destroy the session and redirect the user to GET /. If the user does not
    exist, respond with a 403 HTTP status.
    - `session_id` as a cookie is expected
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """Send user details by session id
    - `session_id` as a cookie is expected
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Generate a token and respond with it
    - Form data with the "email" field expected
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Update the password. If the token is valid"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    password = request.form.get("new_password")
    try:
        reset_token = AUTH.update_password(reset_token, password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
