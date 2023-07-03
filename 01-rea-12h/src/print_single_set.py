#!/usr/bin/python3

from functions import printw, string_to_weekset


if __name__ == "__main__":
    '''
    print a single working set from stdin.
    ex:
    $ ./print_single_set.py
    which set: JJooJJoJJoooJJ

    L M M J V S D
    J J o o J J o
    J J o o o J J
    days worked: 8
    '''
    s_string = input("which set: ")
    printw(string_to_weekset(s_string))
