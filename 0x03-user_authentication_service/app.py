#!/usr/bin/env python3
"""app module"""

from auth import Auth, NoResultFound
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
def logout():
    """logout: User logout function"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user.session_id is None:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect(url_for("index"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Find user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or user.session_id is None:
        abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """get_reset_password_token"""
    try:
        email = request.form.get("email")
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """update user password"""
    try:
        email = request.form.get("email")
        reset_token = request.form.get("reset_token")
        password = request.form.get("new_password")

        AUTH.get_reset_password_token(email)
        AUTH.update_password(reset_token, password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
