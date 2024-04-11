#!/usr/bin/env python3
'''
    Password Encryption and Validation Module
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''
    Generates a salted and hashed password.
    '''
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    Checks whether the provided password matches the hashed password.
    '''
    encoded = password.encode()
    return bcrypt.checkpw(encoded, hashed_password)
