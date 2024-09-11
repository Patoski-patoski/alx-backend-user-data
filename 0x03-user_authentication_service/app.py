#!/usr/bin/env python3
"""app module"""

from auth import Auth
from flask import Flask, jsonify, request

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def set_up():
    """return a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """User registration
    """
    if email and password:
        try:
            email = request.form.get("email")
            password = request.form.get("password")
            AUTH.register_user(email, password)
            payload = {"email": f"{email}", "message": "user created"}
            return jsonify(payload), 201
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
