import os

from java_format_like_python import Formatter


def test_format1():
    path = os.path.join(os.path.dirname(__file__), "test_file.java")
    lines = [line for line in open(path).readlines()]
    new_lines = Formatter().format(lines)
    print(new_lines)
