from base64 import urlsafe_b64encode
from os import urandom

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_or_create_salt(size: int, filename: str = "passwordmanager.salt") -> bytes:
    try:
        salt_file = open(filename, "rb")
        salt = salt_file.read()
        salt_file.close()
        return salt
    except FileNotFoundError:
        salt_file = open(filename, "wb")
        salt = urandom(size)
        salt_file.write(salt)
        salt_file.close()
        return salt


def generate_key(password: str) -> bytes:
    password_byte = password.encode()
    salt = get_or_create_salt(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = urlsafe_b64encode(kdf.derive(password_byte))
    return key


def encrypt(data_string: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(data_string.encode())


def decrypt(data: bytes, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()
