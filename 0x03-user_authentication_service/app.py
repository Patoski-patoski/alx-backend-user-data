#!/usr/bin/env python3
"""app module"""

from auth import Auth
from flask import Flask, jsonify, request, abort, make_response
from sqlalchemy.exc import InvalidRequestError


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def set_up():
    """return a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """User registration route"""
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """login: User login route"""
    email = request.form.get("email")
    password = request.form.get("password")

    if email and password:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response
        else:
            abort(401)
    else:
        abort(401)


if __name__ == "__main__":
    AUTH = Auth()
    app.run(host="0.0.0.0", port="5000", debug=True)
