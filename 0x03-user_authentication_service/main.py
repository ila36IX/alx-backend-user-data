#!/usr/bin/env python3
"""
Test querying the web server end-points
"""
import requests
import json


base_url = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """test registring new user"""
    payload = {"email": email, "password": password}
    r = requests.post(base_url+"/users", data=payload)
    assert r.status_code == 200, "wrong status code"
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:
        assert False, "The response is not a json format"
    assert data.get("email") == email, "json doesn't conatian the right email"
    assert data.get("message") == "user created", "json doesn't conatian the\
    right message"


def log_in_wrong_password(email: str, password: str) -> None:
    """Test log in using wrong password"""
    payload = {"email": email, "password": password}
    r = requests.post(base_url+"/sessions", data=payload)
    assert r.status_code == 401, "wrong status code"


def log_in(email: str, password: str) -> str:
    """Test log in function and session id is correctly reponsed"""
    payload = {"email": email, "password": password}
    r = requests.post(base_url+"/sessions", data=payload)
    assert r.status_code == 200, "wrong status code"
    session_id = r.cookies.get('session_id')
    assert session_id, "The response doesn't contain the session_id cookie"
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:
        assert False, "The response is not a json format"
    assert data.get("email") == email, "json doesn't conatian the right email"
    assert data.get("message") == "logged in", "The response json doesn't\
    conatian the right message"
    return session_id


def profile_unlogged() -> None:
    """Test if sesion id represente a real user"""
    r = requests.get(base_url+"/profile")
    assert r.status_code == 403, "wrong status code"
    wrong_session = {"session_id": "blablab13"}
    r = requests.get(base_url+"/profile", cookies=wrong_session)
    assert r.status_code == 403, "wrong status code"


def profile_logged(session_id: str) -> None:
    """Test if session responed by login is valid"""
    session = {"session_id": session_id}
    r = requests.get(base_url+"/profile", cookies=session)
    assert r.status_code == 200, "wrong status code"
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:
        assert False, "The response is not a json format"
    assert data.get("email"), "json doesn't conatian email"


def log_out(session_id: str) -> None:
    """Test session_id getting destroyed in logout"""
    session = {"session_id": session_id}
    link = base_url+"/sessions"
    r = requests.delete(link, cookies=session, allow_redirects=False)
    assert r.status_code == 302, "wrong status code"
    assert r.headers.get("Location") == "/", "Wrong redirection url"
    r = requests.get(base_url+"/profile", cookies=session)
    assert r.status_code == 403, "wrong status code"


def reset_password_token(email: str) -> str:
    """Test reset pwd contain form data with the email field"""
    payload = {"email": email}
    r = requests.post(base_url+"/reset_password", data=payload)
    assert r.status_code == 200, "wrong status code"
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:
        assert False, "The response is not a json format"
    assert data.get("email") == email, "json doesn't conatian the right email"
    token = data.get("reset_token")
    assert token, "json doesn't contain reset_token"
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating pwd using reset_token"""
    payload = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
            }
    r = requests.put(base_url+"/reset_password", data=payload)
    assert r.status_code == 200, "wrong status code"
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:
        assert False, "The response is not a json format"
    assert data.get("email") == email, "json doesn't conatian the right email"
    assert data.get("message") == "Password updated", "json doesn't conatian\
            the right message"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    session_id = log_in(EMAIL, PASSWD)
    profile_unlogged()
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    session_id = log_in(EMAIL, NEW_PASSWD)
