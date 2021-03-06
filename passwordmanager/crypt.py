from base64 import urlsafe_b64encode
from os import urandom

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .files import read_file, write_file

callback_salt_created = print
default_salt_filename = "passwordmanager.salt"


def get_or_create_salt(size: int, filename: str = default_salt_filename) -> bytes:
    """Liest das Salt zum Ver-und Entschlüsseln aus einer Datei, oder erstellt die Datei falls sie nicht existiert"""
    try:
        return read_file(filename, "rb")
    except FileNotFoundError:
        salt = urandom(size)
        write_file(filename, salt, "wb")
        callback_salt_created(f"Salt-Datei '{filename}' wurde erstellt. Diese wird zum Entschlüsseln benötigt")
        return salt


def generate_key(password: str) -> bytes:
    """Generiert aus einem Passwort mit einem Salt einen Schlüssel zum Ver- und Entschlüsseln von Daten"""
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
    """Verschlüsselt Daten"""
    fernet = Fernet(key)
    return fernet.encrypt(data_string.encode())


def decrypt(data: bytes, key: bytes) -> str:
    """Entschlüsselt Daten"""
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()
