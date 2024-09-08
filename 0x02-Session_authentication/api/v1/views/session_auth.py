#!/usr/bin/env python3
"""session auth.py module"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def handle_routes():
    """handles all routes for the Session authentication"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email is None or len(email) == 0:
            return jsonify({"error": "email missing"}), 400

        if password is None or len(password) == 0:
            return jsonify({"error": "password missing"}), 400

        user = User()
        user_instance = user.search({"email": email})
        if user_instance == []:
            return jsonify({"error": "no user found for this email"}), 404

        user = user_instance[0]
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth

        session_id = auth.create_session(user.id)
        resp = jsonify(user.to_json())
        resp.set_cookie(getenv("SESSION_NAME"), session_id)
        return resp
