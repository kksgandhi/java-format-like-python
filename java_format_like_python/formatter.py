from __future__ import annotations

import re
from functools import partial
from textwrap import dedent

from .utils import (
    append,
    indent_level,
    is_ignorable,
    next_indent_level,
    replace_beginning_with_semicolons,
)


class Formatter:
    def __init__(
        self, padding: int = 80, semicolons: bool = False, only_semicolons: bool = False
    ) -> None:
        self.padding = padding
        self.semicolons = semicolons
        self.only_semicolons = only_semicolons

    def format(self, lines: list[str]) -> list[str]:
        #  creating a function that removes symbols and carriage return from the end
        remove_symbols = partial(re.sub, r" *(;\n|{\n|[;}]*\n)", r"")

        #  removing symbols from every line
        lines_no_symbols = [str(remove_symbols(line)) for line in lines]

        #  you cannot modify a list inside a loop. So I create a copy
        new_lines = []

        for i, line in enumerate(lines_no_symbols):
            #  creating a function that extends my append function
            #  defaults the "line" and "padding" arguments
            append_partial = partial(append, line, self.padding)

            #  if the line is not ignorable or if the "only_semicolons" flag is not on
            if not is_ignorable(str(line)) and not self.only_semicolons:
                cur_indent = indent_level(line)
                next_indent = next_indent_level(i, lines)
                #  Determining the indent difference between this line and the next
                indent_diff = next_indent - cur_indent

                if indent_diff == 0:
                    #  no difference. Just add a semicolon
                    line = append_partial(";")
                elif indent_diff == 1:
                    #  Next line is indented. Add a bracket
                    line = append_partial("{")
                elif indent_diff > 1:
                    #  Some sort of error
                    raise ValueError(
                        dedent(
                            f"""
                        Unexpected indent after line {i}:
                        {line}
                        This program cannot deal with multiline comments
                        Maybe that was it?
                        """
                        )
                    )
                elif indent_diff < 0:
                    #  the next line is unindented
                    #  add a semicolon and the necessary amount of close brackets
                    line = append_partial(";" + "}" * int(-1 * indent_diff))

            #  if the semicolon flag was active
            if self.semicolons or self.only_semicolons:
                line = replace_beginning_with_semicolons(line)

            #  append the modified line to new_lines since lines can't be modified from here
            new_lines.append(line)

        return new_lines
