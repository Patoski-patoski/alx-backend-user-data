#!/usr/bin/env python3
"""app module"""

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/")
def set_up():
    """return a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    email = request.form.get("email")
    password = request.form.get("password")

    if email and password:
        try:
            AUTH.register_user(email, password)
            payload = {"email": f"{email}", "message": "user created"}
            return jsonify(payload), 201
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"message": "email and password required"}), 400


if __name__ == "__main__":
    from auth import Auth

    AUTH = Auth()
    app.run(host="0.0.0.0", port="5000")
