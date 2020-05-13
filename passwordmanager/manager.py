from .crypt import generate_key, decrypt, encrypt
from .entry import Entry
from .files import read_file, write_file


def entries_from_string(from_string: str):
    """Erzeugt eine Liste mit Einträgen aus einem String"""
    lines = from_string.splitlines()
    entries = []
    if len(lines) <= 2:
        return entries
    line_nums = lines[0].split(",")  # Erste Zeile gibt an, wie viele Zeilen jeder Eintrag belegt
    line = 1
    for n in line_nums:
        n = int(n)
        entries.append(Entry("\n".join(lines[line:line + n])))  # Entry-Objekt aus Zeilen erstellen
        line += n
    return entries


class Manager:
    def __init__(self, from_string: str = None):
        self._entries = entries_from_string(from_string) if from_string else []

    def to_string(self) -> str:
        """Erzeugt aus den Einträgen einen String zum Speichern"""
        line_nums = []
        lines = []
        for entry in self._entries:
            string = entry.to_string()
            lines.append(string)
            line_nums.append(str(string.count("\n") + 1))
        return ','.join(line_nums) + "\n" + "\n".join(lines)

    def add_entry(self, entry):
        self._entries.append(entry)

    def remove_entry(self, entry):
        self._entries.remove(entry)

    def find_entries(self, search):
        """Gibt Einträge zurück, die einen Suchbegriff im Namen haben"""
        return list(filter(lambda e: search in e.name, self._entries))

    def get_entries(self):
        return self._entries[:]


def open_manager_from_file(filename: str, key: bytes = None, password: str = None) -> Manager:
    """Liest eine Datei ein, entschlüsselt den Inhalt mit Passwort oder Schlüssel und erzeugt ein Manager-Objekt"""
    if password and not key:
        key = generate_key(password)
    return Manager(decrypt(read_file(filename), key))


def save_manager_to_file(manager: Manager = Manager(), filename: str = None, key: bytes = None, password: str = None):
    """Verschlüsselt den Inhalt eines Manager-Objekts mit Passwort oder Schlüssel und speichert es als Datei"""
    if password and not key:
        key = generate_key(password)
    write_file(filename, encrypt(manager.to_string(), key))
