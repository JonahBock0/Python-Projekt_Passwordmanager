def entries_from_string(from_string: str):
    return []


class Manager:
    def __init__(self, from_string: str = None):
        self.entries = entries_from_string(from_string) if from_string else []

    def to_string(self):
        return ""
