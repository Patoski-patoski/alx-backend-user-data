#!/usr/bin/env python3
"""DB module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """To hashed the user password
    Args:
        password (str): string to be hashed
    Returns:
        byte: hashed password in bytes
    """
    # if not isinstance(password, str):
    #     return
    b_password = password.encode()
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(b_password, salt)
    return hashed_password
