#!/usr/bin/env python3
""" Contains the authentication systems
"""
import bcrypt
from typing import Optional


salt = bcrypt.gensalt()


def _hash_password(password: str) -> Optional[bytes]:
    """ Method hashes a password """
    if password is None:
        return None
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
