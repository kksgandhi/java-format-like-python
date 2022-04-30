from __future__ import annotations

import re


def indent_level(line: str) -> float:
    """
    Returns the 'indent level' of a line
    Assumes line is indented with 4 spaces
    """
    indent_count = 0
    for char in line:
        if char == " ":
            indent_count += 1
        else:
            break
    return indent_count / 4.0


def is_ignorable(line: str) -> bool:
    """
    Returns True if the line is a java comment (starts with //)
    or if the line is only spaces
    """
    if re.match(r" *[^ /]+ */", line):
        raise Exception(
            "This program cannot deal with comments on the same line as code"
        )
    return True if re.match(r" *$", line) or re.match(r" */", line) else False


def next_indent_level(index: int, lines: list[str]) -> float:
    """
    Returns the indent level of the next non-ignorable line
    """
    for i in range(index + 1, len(lines)):
        if not is_ignorable(lines[i]):
            return indent_level(lines[i])
    return 0


def append(line: str, new_len: int, string_to_append: str) -> str:
    """
    Pads the line with the appropriate amount of spaces
    Then appends string_to_append
    """
    while len(line) < new_len:
        line += " "

    return line + string_to_append


def replace_beginning_with_semicolons(line: str) -> str:
    """
    Replaces the spaces in the beginning of a line with semicolons
    The repl param in re.sub can be a function
    This lambda returns a string of semicolons the size of the starting spaces
    """
    return re.sub(r"^ *", lambda x: ";" * len(x.group()), line)
