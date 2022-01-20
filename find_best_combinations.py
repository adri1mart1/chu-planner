from openpyxl import Workbook, load_workbook
import itertools
import os
from time import sleep


THREAD_TOTAL_WEEK_NUMBER = 12
PERSON_NUMBER = 5

# 1 person included
MIN_PERSON_NUMBER_WORKING_PER_WEEKEND = 1
# 2 persons included
MAX_PERSON_NUMBER_WORKING_PER_WEEKEND = 2

MIN_PERSON_NUMBER_WORKING_PER_WORKING_DAY = 1
MAX_WEEKLY_WORKING_HOURS = 48
ONE_DAY_WORKING_HOUR = 12
WORKING_DAY = 'J'
DAY_OFF = '-'

variant_list = []
valid_res = []

results_dir = "output"
variant_dir = os.path.join(results_dir, "variants_12w")
combination_dir = os.path.join(results_dir, "combinations")
weeks_text_file = os.path.join(variant_dir, "12-weeks.txt")
valid_result_file = os.path.join(combination_dir, "valid-results-12w.txt")
invalid_result_file = os.path.join(combination_dir, "invalid-results-12w.txt")



def detect_if_valid_number_of_persons_per_weekend(v) -> bool:
    assert(len(v[0])%7 == 0)
    week_number = int(len(v[0])/7)
    for i in range(0, week_number):
        # person_working_per_week_end -> res
        res = 0
        for p in range(0, PERSON_NUMBER):
            if v[p][7*i+5] != v[p][7*i+6]:
                raise ValueError("Error, variant {}, we have detected a person working only one "
                                 "day in the weekend".format(v))
            # checking saturday (+5)
            if v[p][7*i+5] == WORKING_DAY:
                res = res+1
        if res < MIN_PERSON_NUMBER_WORKING_PER_WEEKEND or res > MAX_PERSON_NUMBER_WORKING_PER_WEEKEND:
            # print("Variant {} is invalid because there are {} persons working on the {}th weekend".format(v, res, i+1))
            return False
    return True


def detect_if_one_person_per_working_day(v):
    week_number = int(len(v[0]) / 7)
    for i in range(0, week_number):
        for d in range(0, 5):
            res = 0
            for p in range(0, PERSON_NUMBER):
                if v[p][7*i+d] == WORKING_DAY:
                    res = res+1
                    break
            # print("number of persons working on day {} -> {}".format(i+1, res))
            if res < MIN_PERSON_NUMBER_WORKING_PER_WORKING_DAY:
                # print("No sufficient working person number on day {} on Variant {}".format(i+1, v))
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
                    res = res+1
            if res == 1:
                end_res = end_res + 1
    return end_res


def evaluate_variant(v) -> bool:
    if not detect_if_valid_number_of_persons_per_weekend(v):
        return False
    if not detect_if_one_person_per_working_day(v):
        return False
    cnt = count_number_of_one_person_per_day_per_working_day(v)
    # only keep result if there is no day with only one person working
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
        idx = idx + 1
    print("Error !!!!!!!!!!")
    print("get_shift_index failed with variant_list {} and th {}".format(variant_list, th))
    return 0


def load_wset_from_file(filename):
    print("Loading wset from {}".format(filename))
    r = []
    with open(filename) as file:
        for line in file:
            r.append(tuple(line.split(' ')[-1].rstrip()))
    return set(r)


def save_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content)


if __name__ == '__main__':

    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(combination_dir, exist_ok=True)

    # for each variant, we generate all combinations
    # for each combination, we count how many person is working per day, sort it and get
    # the best result.

    # we load all variants
    wset = load_wset_from_file(weeks_text_file)
    n_w = int(len(next(iter(wset)))/7)

    cnt = 0
    lenwset = len(wset)
    for s in wset:
        cnt = cnt+1

        variant_list = []
        valid_res = []
        # print("thread is {}".format(s))
        # split each weeks
        for i in range(0, n_w):
            variant_list.append(s[7*i:] + s[:7*i])
        # print(variant_list)

        ''' get all variants based on the number of person working
            ex: say we have 2 persons working and we have the variant_list defined above,
            we will have these variants:
            personA: Th1 personB: Th2
            personA: Th1 personB: Th3
            personA: Th2 personB: Th3
        '''
        all_variants = list(itertools.combinations(variant_list, PERSON_NUMBER))

        ''' for each variant, detect if the variant is interesting '''
        for i in range(len(all_variants)):
            evaluate_variant(all_variants[i])

        print("{}/{} - possible variants: {}/{}".format(cnt, lenwset, len(valid_res), len(all_variants)))
        # new_list = sorted(valid_res, key=lambda d: d['cnt_1p'])

        if len(valid_res) == 0:
            # save_to_file(invalid_result_file, "NO_RES {} {} ".format(cnt, ''.join(s)))
            continue
        else:
            top = valid_res[0]
            save_to_file(valid_result_file, "********\n")
            save_to_file(valid_result_file, "shift: {}\n".format(''.join(s)))
            for th in top['thread']:
                save_to_file(valid_result_file, "s{}: {}\n".format(get_shift_index(th), ''.join(th)))

            count_number_of_one_person_per_day_per_working_day(top['thread'])
            save_to_file(valid_result_file, "1-person working num: {}/{}\n".format(top['cnt_1p'], THREAD_TOTAL_WEEK_NUMBER*7))
