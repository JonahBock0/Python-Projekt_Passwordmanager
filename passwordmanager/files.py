def check_file(filename: str):
    """Gibt zurück, ob eine Datei existiert"""
    try:
        file = open(filename, "r")
        file.close()
    except FileNotFoundError:
        return False
    return True


def read_file(filename: str, mode: str = "rb"):
    """Liest den Inhalt einer Datei aus und gibt ihn zurück"""
    file = open(filename, mode)
    content = file.read()
    file.close()
    return content


def write_file(filename: str, content, mode: str = "wb"):
    """Schreibt den übergebenen Inhalt in eine Datei"""
    file = open(filename, mode)
    file.write(content)
    file.close()
