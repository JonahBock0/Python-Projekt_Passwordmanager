def read_file(filename: str, mode: str = "rb"):
    file = open(filename, mode)
    content = file.read()
    file.close()
    return content


def write_file(filename: str, content, mode: str = "wb"):
    file = open(filename, mode)
    file.write(content)
    file.close()