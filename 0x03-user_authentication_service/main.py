#!/usr/bin/env python3
"""main module"""

import requests


endpoints = {
    "users": "http://localhost:5000/users",
    "sessions": "http://localhost:5000/sessions",
    "profile": "http://localhost:5000/profile",
    "reset_password": "http://localhost:5000/reset_password",
}


def register_user(email: str, password: str) -> None:
    response = requests.post(
        url=endpoints["users"], data={"email": email, "password": password}
    )
    assert response.status_code == 201


def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(
        url=endpoints["sessions"], data={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    response = requests.post(
        url=endpoints["sessions"], data={"email": email, "password": password}
    )
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    response = requests.get(url=endpoints["profile"])
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    response = requests.get(
        url=endpoints["profile"], cookies={"session_id": session_id}
    )
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    response = requests.delete(
        url=endpoints["sessions"], cookies={"session_id": session_id}
    )
    assert response.cookies.get("session_id") is None


def reset_password_token(email: str) -> str:
    response = requests.post(
        url=endpoints["reset_password"], data={"email": email})
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
