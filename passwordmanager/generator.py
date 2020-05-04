import secrets
import string


def generate_password(length: int,
                      letters: bool = True, digits: bool = True, punctuation: bool = True, space: bool = True,
                      exclude: str = ""):
    password_chars = ' ' if space else ''
    if letters:
        password_chars += string.ascii_letters
    if digits:
        password_chars += string.digits
    if punctuation:
        password_chars += string.punctuation
    for c in exclude:
        password_chars = password_chars.replace(c, '')
    print(password_chars)
    password = ""
    for i in range(length):
        password += secrets.choice(password_chars)
    return password
