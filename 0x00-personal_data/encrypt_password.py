#!/usr/bin/env python3
'''
   5. Encrypting passwords
   6. Check valid password
'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''
    Hashes a password using bcrypt.

    Arguments:
    password -- The password to hash.

    Returns:
    A salted, hashed password as a byte string.
    '''
    pass_encoded = password.encode('utf-8')
    pass_hashed = bcrypt.hashpw(pass_encoded, bcrypt.gensalt())
    return pass_hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    Checks if a given password matches its hashed version.

    Arguments:
    hashed_password -- The hashed password (bytes).
    password -- The plaintext password (str).

    Returns:
    True if the password matches the hashed password, False otherwise.
    '''
    pass_encoded = password.encode('utf-8')
    return bcrypt.checkpw(pass_encoded, hashed_password)
