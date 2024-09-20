#!/usr/bin/env python3
""" Main 4
"""
from flask import Flask, request
from api.v1.auth.session_auth import SessionAuth
from models.user import User

""" Create a user test """
user_email = "alien@hbtn.io"
user_clear_pwd = "123"

user = User()
user.email = user_email
user.password = user_clear_pwd
user.save()
user.load_from_file
