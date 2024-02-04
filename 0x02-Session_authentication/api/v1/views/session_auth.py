#!/usr/bin/env python3
""" Session authentication specific views
"""
from os import getenv
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, make_response


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def session_login():
    """ Handles user login session """
    email = request.form.get("email")
    pwd = request.form.get("password")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if pwd is None or pwd == "":
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(pwd):
            from api.v1.app import auth
            session_id = auth.create_session(user.get("id"))
            session_name = getenv('SESSION_NAME')
            response = make_response(jsonify(user.to_json()))
            response.set_cookie(session_name, session_id)
            return response
        return jsonify({"error": "wrong password"}), 401
