import hashlib


def encrypt_password(password: str):
    # Compute SHA-1 hash
    return hashlib.sha1(password.encode()).hexdigest()


# Output the hashed password
# print(encrypt_password('mohamed123456'))
