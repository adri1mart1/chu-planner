#!/usr/bin/python3

import sys
sys.path.append('../../00-common/src/')

from itertools import combinations
from functions import printw, load_wset_from_file, save_to_file
from os.path import join
from os import makedirs


THREAD_TOTAL_WEEK_NUMBER = 12
PERSON_NUMBER = 5

''' 1 person included '''
MIN_PERSON_NUMBER_WORKING_PER_WEEKEND = 1
''' 2 persons included '''
MAX_PERSON_NUMBER_WORKING_PER_WEEKEND = 2

MIN_PERSON_NUMBER_WORKING_PER_WORKING_DAY = 1
MAX_WEEKLY_WORKING_HOURS = 48
ONE_DAY_WORKING_HOUR = 12
WORKING_DAY = 'J'

variant_list = []
valid_res = []

results_dir = "../output"
variant_dir = join(results_dir, "variants_12w")
combination_dir = join(results_dir, "combinations")
weeks_text_file = join(variant_dir, "12-weeks.txt")
valid_result_file = join(combination_dir, "valid-results-12w.txt")
invalid_result_file = join(combination_dir, "invalid-results-12w.txt")



def detect_if_valid_number_of_persons_per_weekend(v) -> bool:
    assert(len(v[0])%7 == 0)
    week_number = int(len(v[0])/7)
    for i in range(0, week_number):
        ''' person_working_per_week_end -> res '''
        res = 0
        for p in range(0, PERSON_NUMBER):
            if v[p][7*i+5] != v[p][7*i+6]:
                raise ValueError("Error, variant {}, we have detected a person working only one "
                                 "day in the weekend".format(v))
            ''' checking saturday (+5) '''
            if v[p][7*i+5] == WORKING_DAY:
                res += 1
        if res < MIN_PERSON_NUMBER_WORKING_PER_WEEKEND or res > MAX_PERSON_NUMBER_WORKING_PER_WEEKEND:
            return False
    return True


def detect_if_one_person_per_working_day(v):
    week_number = int(len(v[0]) / 7)
    for i in range(0, week_number):
        for d in range(0, 5):
            res = 0
            for p in range(0, PERSON_NUMBER):
                if v[p][7*i+d] == WORKING_DAY:
                    res += 1
                    break
            if res < MIN_PERSON_NUMBER_WORKING_PER_WORKING_DAY:
                return False
    return True


def count_number_of_one_person_per_day_per_working_day(v) -> int:
    end_res = 0
    week_number = int(len(v[0])/7)
    for i in range(0, week_number):
        for d in range(0, 5):
            res = 0
            for p in range(0, PERSON_NUMBER):
                if v[p][7*i+d] == WORKING_DAY:
                    res += 1
            if res == 1:
                end_res += 1
    return end_res


def evaluate_variant(v) -> bool:
    if not detect_if_valid_number_of_persons_per_weekend(v):
        return False

    if not detect_if_one_person_per_working_day(v):
        return False

    cnt = count_number_of_one_person_per_day_per_working_day(v)
    ''' only keep result if there is no day with only one person working '''
    if cnt == 0:
        return False

    new_res = dict()
    new_res['cnt_1p'] = cnt
    new_res['thread'] = v
    valid_res.append(new_res)
    return True


def detect_if_thread_respect_max_hours_smooth(th):
    m = MAX_WEEKLY_WORKING_HOURS / ONE_DAY_WORKING_HOUR
    for i in range(0, len(th)-7):
        cnt = th.count(WORKING_DAY, i, i+7)
        if cnt > m:
            print("Too many hours {}h detected at index: {}".format(cnt*12, i))
            return False
    return True


def get_shift_index(th) -> int:
    idx = 1
    for v in variant_list:
        if th == v:
            return idx
        idx += 1
    raise ValueError("get_shift_index failed with variant_list {} and th {}".format(variant_list, th))


if __name__ == '__main__':

    makedirs(results_dir, exist_ok=True)
    makedirs(combination_dir, exist_ok=True)

    '''
    for each variant, we generate all combinations
    for each combination, we count how many person is working per day, sort it and get
    the best result '''

    ''' we load all variants '''
    wset = load_wset_from_file(weeks_text_file)
    assert(len(wset) >= 0)

    ''' number of week based on the first element '''
    n_w = int(len(next(iter(wset)))/7)

    cnt = 0
    lenwset = len(wset)
    min_res = 9999

    for s in wset:
        cnt += 1

        variant_list = []
        valid_res = []

        ''' split each weeks '''
        for i in range(0, n_w):
            variant_list.append(s[7*i:] + s[:7*i])

        '''
        get all variants based on the number of person working
        ex: say we have 2 persons working and we have the variant_list defined above,
        we will have these variants:
        personA: Th1 personB: Th2
        personA: Th1 personB: Th3
        personA: Th2 personB: Th3 '''
        all_variants = list(combinations(variant_list, PERSON_NUMBER))

        ''' for each variant, detect if the variant is interesting '''
        for i in range(len(all_variants)):
            evaluate_variant(all_variants[i])

        print("{}/{} - possible variants: {}/{}".format(cnt, lenwset, len(valid_res), len(all_variants)))

        ''' if no valid result, continue looping '''
        if len(valid_res) == 0:
            continue

        ''' we have some valid results '''
        top = valid_res[0]
        save_to_file(valid_result_file, "********\nshift: {}\n".format(''.join(s)))
        for th in top['thread']:
            save_to_file(valid_result_file, "s{}: {}\n".format(get_shift_index(th), ''.join(th)))

        count_number_of_one_person_per_day_per_working_day(top['thread'])
        save_to_file(valid_result_file, "1-person working num: {}/{}\n".format(top['cnt_1p'], THREAD_TOTAL_WEEK_NUMBER*7))

        if min_res > int(top['cnt_1p']):
            min_res = int(top['cnt_1p'])

    print("find best combination search finished, best result is {} days with one person working".format(min_res))
