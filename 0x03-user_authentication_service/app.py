#!/usr/bin/env python3
""" Contains the flask app
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def message() -> str:
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def user() -> str:
    """ Registers a user """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    msg = {"email": email, "message": "user created"}
    return jsonify(msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
