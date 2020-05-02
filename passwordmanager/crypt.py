from cryptography.fernet import Fernet


def generate_key(password: str):
    pass


def encrypt(data_string: str, key: bytes):
    fernet = Fernet(key)
    return fernet.encrypt(data_string.encode())


def decrypt(data: bytes, key: bytes):
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()
