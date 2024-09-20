#!/usr/bin/env python3
# """ Main 4
# """
# from flask import Flask, request
# from api.v1.auth.session_auth import SessionAuth
# from models.user import User
#
# """ Create a user test """
# user_email = "alien@hbtn.io"
# user_clear_pwd = "123"
#
# user = User()
# user.email = user_email
# user.password = user_clear_pwd
# user.save()
# user.load_from_file
#!/usr/bin/env python3
#!/usr/bin/python3
""" Check response
"""
import requests

if __name__ == "__main__":
    r = requests.get('http://0.0.0.0:5000/api/v1/users')
    if r.status_code != 401:
        print("Wrong status code: {}".format(r.status_code))
        exit(1)
    if r.headers.get('content-type') != "application/json":
        print("Wrong content type: {}".format(r.headers.get('content-type')))
        exit(1)
    try:
        r_json = r.json()
        
        if len(r_json.keys()) != 1:
            print("Not the right number of element in the JSON: {}".format(r_json))
            exit(1)
        
        error_value = r_json.get('error')
        if error_value is None:
            print("Missing 'error' key in the JSON: {}".format(r_json))
            exit(1)
        if error_value != "Unauthorized":
            print("'error' doesn't have the right value: {}".format(error_value))
            exit(1)
            
        print("OK", end="")
    except:
        print("Error, not a JSON")
