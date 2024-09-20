#!/usr/bin/env python3
""" Main 4
"""
from flask import Flask, request
from api.v1 import app


for s in dir(app):
    print(len(getattr(app, s).__doc__))
