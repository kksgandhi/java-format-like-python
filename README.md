# java-format-like-python

## Simply run this program on your java files to turn them into python-esque beauties!

![Java formatted like python](https://i.imgur.com/wG51k7v.png)

<https://www.reddit.com/r/ProgrammerHumor/comments/2wrxyt/a_python_programmer_attempting_java/>

## Install

```sh
pip install https://github.com/kksgandhi/java-format-like-python
```

<!-- or, pip install java-format-like-python after being published on pypi -->

## Usage

To format in-place:

```sh
j2p-fmt filename.java -i
```

## Assumes your program is indented with spaces

To get information for help  and some other flags:

```shellsession
$ j2p-fmt -h
usage: j2p-fmt [-h] [-i] [-p PADDING] [-s] [-S] [-V] file

Simply run this program on your java files to turn them into python-esque
beauties!

positional arguments:
  file        file to be modified

optional arguments:
  -h, --help  show this help message and exit
  -i          modify file in place and backup original file
  -p PADDING  specifies the amount of padding to use before semicolons.
              Default 80
  -s          replace beginning of every line with semicolons
  -S          only replace beginning of every line with semicolons
  -V          show program's version number and exit

```

## Development

I accept pull requests. Todo:

* Deal with tab indenting instead of spaces

* Deal with a larger variety of comment types

* Other languages?
