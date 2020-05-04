from passwordmanager.entry import Entry


def entries_from_string(from_string: str):
    lines = from_string.splitlines()
    entries = []
    line_nums = lines[0].split(",")
    line = 1
    for n in line_nums:
        n = int(n)
        entries.append(Entry("\n".join(lines[line:line + n])))
        line += n
    return entries


class Manager:
    def __init__(self, from_string: str = None):
        self.entries = entries_from_string(from_string) if from_string else []

    def to_string(self):
        line_nums = []
        lines = []
        for entry in self.entries:
            string = entry.to_string()
            lines.append(string)
            line_nums.append(str(string.count("\n") + 1))
        return ','.join(line_nums) + "\n" + "\n".join(lines)
