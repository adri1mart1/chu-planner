#!/usr/bin/python3

import sys
sys.path.append('../../00-common/src/')

from as_ptmc_functions import *
from functions import *
from os.path import isfile

if __name__ == "__main__":

    file = "../output/variants_12w/alt-18-weeks.txt"

    if not isfile(file):
        raise ValueError("Error, file {} missing".format(file))

    with open(file) as f:
        for line in f:
            print('*****************************************')
            print(line.rstrip())
            printw_asptmc(string_to_weekset(line), detailed_hours=True)
