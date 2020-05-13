import string
from secrets import choice


def generate_password(length: int, exclude: str = "",
                      letters: bool = True, digits: bool = True, punctuation: bool = True, space: bool = True) -> str:
    """Passwort in ausgewählter Länge generieren,
    aus auswählbaren Zeichen (Buchstaben, Zahlen, Sonderzeichen, Leerzeichen) und ausgeschlossenen Zeichen"""
    password_chars = ' ' if space else ''
    if letters:
        password_chars += string.ascii_letters
    if digits:
        password_chars += string.digits
    if punctuation:
        password_chars += string.punctuation
    for c in exclude:
        password_chars = password_chars.replace(c, '')
    password = ""
    for i in range(length):
        password += choice(password_chars)
    return password
