#!/usr/bin/env python3
""" Contains the flask app
"""
from flask import Flask, jsonify, request, abort, make_request
from auth import Auth
from sqlalchemy.exc import NoResultFound

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def message():
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def user():
    """ Registers a user """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        return "No email and password"
    try:
        AUTH.register_user(email, password)
        message = {"email": email, "message": "user created"}
        return jsonify(message), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """ Handles the login operation as well as session management """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        return "No email or password"
    try:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            msg = {"email": f"{email}", "message": "logged in"}
            response = make_response(jsonify(msg), 200)
            response.set_cookie("session_id", session_id)
            return response
    except NoResultFound:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
