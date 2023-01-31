import argparse
import os
import sys

from . import Formatter, __version__


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simply run this program on your java files to turn them into python-esque beauties!"
    )

    parser.add_argument("file", help="file to be modified")

    parser.add_argument(
        "-i",
        dest="inplace",
        action="store_true",
        help="modify file in place and backup original file",
    )

    parser.add_argument(
        "-p",
        dest="padding",
        action="store",
        default=80,
        type=int,
        help="specifies the amount of padding to use before semicolons. Default 80",
    )

    parser.add_argument(
        "-s",
        dest="semicolons",
        action="store_true",
        help="replace beginning of every line with semicolons",
    )

    parser.add_argument(
        "-S",
        dest="only_semicolons",
        action="store_true",
        help="only replace beginning of every line with semicolons",
    )
    parser.add_argument("-V", action="version", version=__version__)

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    #  Reading the file in
    lines = [line for line in open(args.file).readlines()]

    try:
        new_lines = Formatter(
            args.padding, args.semicolons, args.only_semicolons
        ).format(lines)
    except ValueError as e:
        print(e.args, file=sys.stderr)
        sys.exit(1)

    #  If not args.inplace then create a new file by appending "_better"
    outfile_name = os.path.splitext(args.file)[0] + "_better.java" if not args.inplace else args.file

    #  writing out the file
    print("\n".join(new_lines), file=open(outfile_name, "w"))

    if args.inplace:
        print("\n".join(lines), file=open(outfile_name + ".backup", "w"))
