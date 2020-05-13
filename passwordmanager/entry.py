def entry_from_string(from_string: str):
    """Erzeugt einen Eintrag aus einem String"""
    lines = from_string.splitlines()
    name = lines[0]
    user = lines[1]
    password = lines[2]
    notes_lines = int(lines[3])
    notes = "\n".join(lines[4:4 + notes_lines])
    attributes = dict()
    attribute_lines = lines[4 + notes_lines:]
    for i in range(0, len(attribute_lines), 2):
        attributes[attribute_lines[i]] = attribute_lines[i + 1]
    return name, user, password, notes, attributes


class Entry:
    def __init__(self, from_string: str = None, name: str = "", user: str = "", password: str = ""):
        if from_string:
            self.name, self.user, self.password, self.notes, self.attributes = entry_from_string(from_string)
        else:
            self.name = name
            self.user = user
            self.password = password
            self.notes = ""
            self.attributes = dict()

    def to_string(self) -> str:
        """Erzeugt aus dem Eintrag einen String"""
        notes_lines = self.notes.count("\n") + 1  # Anzahl der Zeilen, die die Notizen verbrauchen
        attributes = []
        for key, val in self.attributes.items():
            attributes.append(f"{key}\n{val}")
        attributes_string = "\n".join(attributes)
        string = f"{self.name}\n{self.user}\n{self.password}\n{notes_lines}\n{self.notes}\n{attributes_string}"
        return string
