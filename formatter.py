import sys
from functools import partial
import argparse
import re
#  from pprint import pprint as print

def indent_level(line):
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
    return indent_count / 4

def is_ignorable(line):
    """
    Returns True if the line is a java comment (starts with //)
    or if the line is only spaces
    """
    if re.match(r" *[^ /]+ */", line):
        raise Exception("This program cannot deal with comments on the same line as code")
    return True if re.match(r" *$", line) or re.match(r" */", line) else False

def next_indent_level(index, lines):
    """
    Returns the indent level of the next non-ignorable line
    """
    for i in range(index + 1, len(lines)):
        if not is_ignorable(lines[i]):
            return indent_level(lines[i])
    return 0

def append(line, new_len, string_to_append):
    """
    Pads the line with the appropriate amount of spaces
    Then appends string_to_append
    """
    while len(line) < new_len:
        line += " "

    return line + string_to_append

def replace_beginning_with_semicolons(line):
    """
    Replaces the spaces in the beginning of a line with semicolons
    The repl param in re.sub can be a function
    This lambda returns a string of semicolons the size of the starting spaces
    """
    return re.sub(r"^ *", lambda x: ';' * len(x.group()), line)

def main(args):
    #  Reading the file in
    with open(args.file)  as input_file:
        lines = [line for line in input_file.readlines()]

    #  creating a function that removes symbols and carriage return from the end
    remove_symbols = partial(re.sub, r" *(;\n|{\n|[;}]*\n)", r"")

    #  removing symbols from every line
    lines_no_symbols = list(map(remove_symbols, lines))
    #  you cannot modify a list inside a loop. So I create a copy
    new_lines = []

    for i, line in enumerate(lines_no_symbols):
        #  creating a function that extends my append function
        #  defaults the "line" and "padding" arguments
        append_partial = partial(append, line, args.padding)

        #  if the line is not ignorable or if the "only_semicolons" flag is not on
        if not is_ignorable(line) and not args.only_semicolons:
            cur_indent  = indent_level(line)
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
                print("Unexpected indent after line "+str(i))
                print(line)
                print("This program cannot deal with multiline comments\nMaybe that was it?")
                sys.exit(1)
            elif indent_diff < 0:
                #  the next line is unindented
                #  add a semicolon and the necessary amount of close brackets
                line = append_partial(";" + "}" * int(-1 * indent_diff))

        #  if the semicolon flag was active
        if args.semicolons or args.only_semicolons:
            line = replace_beginning_with_semicolons(line)
        #  append the modified line to new_lines since lines can't be modified from here
        new_lines.append(line)

    #  If not args.inplace then create a new file by appending "_better"
    outfile_name = args.file[:-5] + "_better.java" if not args.inplace else args.file

    #  writing out the file
    with open(outfile_name, "w") as outfile:
        for line in new_lines:
            outfile.write(line+"\n")

    if args.inplace:
        with open(outfile_name + ".backup", "w") as outfile:
            for line in lines:
                outfile.write(line)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('file',
            help='file to be modified')

    parser.add_argument('-i',
            dest='inplace',
            action='store_true',
            help='modify file in place and backup original file')

    parser.add_argument('-p',
            dest='padding',
            action='store',
            default=80,
            type=int,
            help='specifies the amount of padding to use before semicolons. Default 80')

    parser.add_argument('-s',
            dest='semicolons',
            action='store_true',
            help='replace beginning of every line with semicolons')

    parser.add_argument('-S',
            dest='only_semicolons',
            action='store_true',
            help='only replace beginning of every line with semicolons')

    args = parser.parse_args()

    main(args)
