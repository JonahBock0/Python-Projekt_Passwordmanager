def entry_from_string(from_string: str):
    name = ""
    user = ""
    password = ""
    notes = ""
    attributes = dict()
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

    def to_string(self):
        lines = 0
        string = ""
        return string, lines
