#!/usr/bin/python3

import sys
sys.path.append('../../00-common/src/')

from ephad_functions import *
from functions import *
from os.path import isfile

if __name__ == "__main__":

    file = "../output/variants_12w/12-weeks.txt"

    if not isfile(file):
        raise ValueError("Error, file {} missing".format(file))

    with open(file) as f:
        for line in f:
            print('*****************************************')
            print(line.rstrip())
            printw_ephad(string_to_weekset(line))
