#!/usr/bin/env python3
"""5. Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """a function called hash_password that takes a password
    string arguments and returns a salted, hashed password,
    which is a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """a function called is_valid that takes a hashed password
    arguments and returns a boolean"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
