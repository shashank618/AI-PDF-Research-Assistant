
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


# Generate password hash
def hash_password(password: str):

    return password_hash.hash(password)


# Verify password
def verify_password(plain_password: str, hashed_password: str):

    return password_hash.verify(
        plain_password,
        hashed_password
    )
