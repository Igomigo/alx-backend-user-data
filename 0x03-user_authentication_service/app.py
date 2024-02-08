#!/usr/bin/env python3
""" Contains the flask app
"""
from flask import Flask, jsonify


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
        return jsonify(message), 400
    except ValueError:
        return jsonify({"message": "email already registered"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
