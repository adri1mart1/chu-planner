#!/usr/bin/python3

from functions import printw, string_to_weekset
from os.path import isfile


if __name__ == "__main__":
    '''
    print a week set from an input file.
    Ex:
    $ cat a.txt
    JJooJJo
    JJoooJJ
    $ ./print_sets.py
    which input file: a.txt

    L M M J V S D
    J J o o J J o
    days worked: 4

    L M M J V S D
    J J o o o J J
    days worked: 4
    '''
    in_file = input("which input file: ")

    if not isfile(in_file):
        raise ValueError("Error, file doesn't exists")

    with open(in_file) as f:
        for line in f:
            printw(string_to_weekset(line))
