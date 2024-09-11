#!/usr/bin/env python3
"""app module"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
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
    """login: User login function"""
    email = request.form.get("email")
    password = request.form.get("password")

    if email and password:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(401)
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """logout: User logout function"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        response = redirect(url_for("index"))
        response.set_cookie("session_id", expires=0)
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
