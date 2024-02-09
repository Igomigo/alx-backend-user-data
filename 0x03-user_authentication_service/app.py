#!/usr/bin/env python3
""" Contains the flask app
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Logs in a user and returns session ID """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
    except KeyError:
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    msg = {"email": email, "message": "logged in"}
    response = make_response(jsonify(msg))

    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ Logs out a user """
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ returns a user profile based on the value of the session_id """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ generates a reset token and stores to the database """
    try:
        email = request.form.get("email")
    except KeyError:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    msg = {"email": f"{email}", "reset_token": f"{reset_token}"}
    return jsonify(msg), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def reset_password() -> str:
    """ PUT /reset_password
    Updates password with reset token
    Return:
        - 400 if bad request
        - 403 if not valid reset token
        - 200 and JSON Payload if valid
    """
    try:
        email = request.form.get("email")
        token = request.form.get("reset_token")
        new_pwd = request.form.get("new_password")
    except KeyError:
        abort(400)

    try:
        AUTH.update_password(token, new_pwd)
    except ValueError:
        abort(403)

    msg = {"email": email, "message": "Password updated"}
    return jsonify(msg), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
