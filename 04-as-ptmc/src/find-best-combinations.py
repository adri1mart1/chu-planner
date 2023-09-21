#!/usr/bin/python3

from itertools import combinations
from as_ptmc_functions import *
from os.path import join
from random import randint

file_jour = join(variant_dir, "jour-18-weeks.txt")
file_nuit = join(variant_dir, "nuit-18-weeks.txt")
file_alt = join(variant_dir, "alt-18-weeks.txt")

threads_jour = []
threads_nuit = []
threads_alt = []

hash_values = {}
min_score_value_all_time = 99999
min_average_value = 9999

TOTAL_WEEK_NUMBER = 18
TOTAL_NUM_PERSON_DAY = 22
TOTAL_NUM_PERSON_DAY_SINGLE = 18
TOTAL_NUM_PERSON_DAY_DOUBLE = TOTAL_NUM_PERSON_DAY - TOTAL_NUM_PERSON_DAY_SINGLE
TOTAL_NUM_PERSON_ALT = 16
TOTAL_NUM_PERSON_NIGHT = 8

MIN_PERSON_IN_7h30_ON_WEEKENDS = 1
MIN_PERSON_IN_7H30_MONDAY_TO_FRIDAY = 2
MIN_PERSON_IN_12H_EACH_DAY = 9

assert (TOTAL_NUM_PERSON_DAY_DOUBLE > 0)


def generate_random_number(max_value) -> int:
    return randint(0, max_value-1)


def get_hash_value(a: int, b: int, c: int) -> int:
    assert(a < 2**14 and b < 2**14 and c < 2**14)
    return (a << 28) + (b << 14) + c


def read_data_from_file(file, thread) -> None:
    with open(file) as f:
        for l in f:
            s = string_to_weekset(l)
            thread.append(l)


def get_week_variants(s):
    variants = []
    for i in range(0, TOTAL_WEEK_NUMBER):
        variants.append(s1[7 * i:] + s1[:7 * i])
    return variants


def get_requirement_score(cs, cd, cn, ca):
    score = 0
    # print("cs: {}".format(len(cs)))
    # print("cd: {}".format(len(cd)))
    # print("cn: {}".format(len(cn)))
    # print("ca: {}".format(len(ca)))

    # print(cd)
    # - 2 persons in 7h30 each day
    # - 1 person in 7h30 saturday and sunday
    # - 9 persons in 12h all week

    for day_n in range(TOTAL_WEEK_NUMBER * 7):
        workers = []
        for person in cd:
            # print("person: {}".format(person))
            # print("person[{}] = {}".format(day_n, person[day_n]))
            workers.append(person[day_n])
        for person in cn:
            workers.append(person[day_n])
        for person in cs:
            workers.append(person[day_n])
        for person in ca:
            workers.append(person[day_n])

        # print("workers:{}".format(workers))

        assert len(workers) == (TOTAL_NUM_PERSON_DAY + TOTAL_NUM_PERSON_NIGHT + TOTAL_NUM_PERSON_ALT)

        count_morning = workers.count('M')
        count_day = workers.count('J')
        # print("Number of person in 7h30 -> {}".format())
        # print("Number of person in 12h -> {}".format())

        # if saturday or sunday
        if ((day_n % 6) == 0) or ((day_n  % 7) == 0):
            if count_morning < MIN_PERSON_IN_7h30_ON_WEEKENDS:
                score += 1
        else:
            if count_morning < MIN_PERSON_IN_7H30_MONDAY_TO_FRIDAY:
                score += 1

        # all times
        if count_day < MIN_PERSON_IN_12H_EACH_DAY:
            score += 1

    # print("score: {}".format(score))
    return score


def checking(s1, s2, s3) -> int:
    """ This is where the fun begins """
    global min_score_value_all_time
    global min_average_value

    # compute week variants
    variants_day = get_week_variants(s1)
    variants_night = get_week_variants(s2)
    variants_alt = get_week_variants(s3)

    assert (len(variants_day) == TOTAL_WEEK_NUMBER)
    assert (len(variants_night) == TOTAL_WEEK_NUMBER)
    assert (len(variants_alt) == TOTAL_WEEK_NUMBER)

    # find all combinations
    combination_day_simple = list(combinations(variants_day, TOTAL_NUM_PERSON_DAY_SINGLE))
    combination_day_double = list(combinations(variants_day, TOTAL_NUM_PERSON_DAY_DOUBLE))
    combination_night = list(combinations(variants_night, TOTAL_NUM_PERSON_NIGHT))
    combination_alt = list(combinations(variants_alt, TOTAL_NUM_PERSON_ALT))

    # print('number of combination day_simple:{} night:{} alt:{} day_double:{}'.format(len(combination_day_simple), len(combination_night),
    #                                                                      len(combination_alt), len(combination_day_double)))

    # for each combination or combination, check min requirements
    cnt = 0
    # total_possibilities = len(combination_day_simple) * len(combination_night) * len(combination_alt) * len(combination_day_double)

    INITIAL_EXPLORED_VALUE = 100
    explored_possibilities_num = INITIAL_EXPLORED_VALUE
    local_min_score = 99999
    local_max_score = 0
    local_average = 0

    while True:
        # First, we explore 100 times if it's worth it to check deeper

        # As there are too many combinations, we are going to use a hash table again and test randomly some possibilities
        for i in range(explored_possibilities_num):
            cs_idx = randint(0, len(combination_day_simple)-1)
            cd_idx = randint(0, len(combination_day_double)-1)
            cn_idx = randint(0, len(combination_night)-1)
            ca_idx = randint(0, len(combination_alt)-1)
            # print("day:[{}/{}] night:[{}/{}] alt:[{}/{}] double:[{}/{}]".format(cs_idx, len(combination_day_simple), cn_idx, len(combination_night), ca_idx, len(combination_alt), cd_idx, len(combination_day_double)))
            score = get_requirement_score(combination_day_simple[cs_idx], combination_day_double[cd_idx], combination_night[cn_idx], combination_alt[ca_idx])
            local_average += score
            cnt += 1
            local_min_score = min(local_min_score, score)
            local_max_score = max(local_max_score, score)
            if i % 1000 == 0:
                print("{}/{} -> best score: {}".format(i, explored_possibilities_num, local_min_score))

            if score < min_score_value_all_time:
                min_score_value_all_time = score
                print("New min score value of all time {}".format(min_score_value_all_time))
                filename = join(combination_dir, "score-{}.txt".format(min_score_value_all_time))
                print("Saving to file {}".format(filename))
                with open(filename, 'w') as f:
                    f.write("s1: {}\n".format(weekset_to_string(s1)))
                    f.write("s2: {}\n".format(weekset_to_string(s2)))
                    f.write("s3: {}\n".format(weekset_to_string(s3)))
                    f.write("\n")
                    f.write("combination_day_simple[cs_idx]\n")
                    for j in range(TOTAL_NUM_PERSON_DAY_SINGLE):
                        f.write("person {} - {}\n".format(j+1, weekset_to_string(combination_day_simple[cs_idx][j])))
                    f.write("\n")
                    f.write("combination_day_double[cd_idx]\n")
                    for j in range(TOTAL_NUM_PERSON_DAY_DOUBLE):
                        f.write("person {} - {}\n".format(j+1, weekset_to_string(combination_day_double[cd_idx][j])))
                    f.write("\n")
                    f.write("combination_night[cn_idx]\n")
                    for j in range(TOTAL_NUM_PERSON_NIGHT):
                        f.write("person {} - {}\n".format(j+1, weekset_to_string(combination_night[cn_idx][j])))
                    f.write("\n")
                    f.write("combination_alt[ca_idx]\n")
                    for j in range(TOTAL_NUM_PERSON_ALT):
                        f.write("person {} - {}\n".format(j + 1, weekset_to_string(combination_alt[ca_idx][j])))
                    f.write("score: {}\n".format(score))

        local_average = local_average / explored_possibilities_num
        print("Explored {} values, scores: min:{} avg:{} max:{}".format(explored_possibilities_num, local_min_score, local_average, local_max_score))
        if explored_possibilities_num == INITIAL_EXPLORED_VALUE:
            if local_average < min_average_value:
                min_average_value = min(min_average_value, local_average)
                explored_possibilities_num = 20000
                continue
            else:
                break
        else:
            break


if __name__ == "__main__":
    print("trying to find best combinations")

    read_data_from_file(file_jour, threads_jour)
    read_data_from_file(file_nuit, threads_nuit)
    read_data_from_file(file_alt, threads_alt)

    count_file_jour = len(threads_jour)
    count_file_nuit = len(threads_nuit)
    count_file_alt = len(threads_alt)

    print(" * count_file_jour: {}".format(count_file_jour))
    print(" * count_file_nuit: {}".format(count_file_nuit))
    print(" * count_file_alt: {}".format(count_file_alt))

    total_possibilities = count_file_jour * count_file_nuit * count_file_alt

    print(" * total_possibilities: {}".format(total_possibilities))

    """
    Say we have about 2000 threads for day, same for night and same for alt, we will get 2000^3 possibilities
    (8 billions). This is a lot so to optimize this a bit, we are going to check randomly a product of all
    combinations. 
    We will take a random number for day, night and alt and create a hash value we will store in a table. 
    If a number is already in the hash table, generate a new one.
    The hash table is define like so:
    random number for days: (14 bits << 28)
    random number for night: (14 bits << 14)
    random number for alt: (14 bits << 0)
    This will create a single number inferior to 64 bits so quite easy to store in a table of int. 
    Why 14 bits ? because 2^14 is 16.384, this is more than enough possibilities to check.
    """

    for i in range(100000):
        x_j = generate_random_number(count_file_jour)
        x_n = generate_random_number(count_file_nuit)
        x_a = generate_random_number(count_file_alt)
        # print(" * random num x_j: {} --- 0x{:08x} --- {:064b}".format(x_j, x_j, x_j))
        # print(" * random num x_n: {} --- 0x{:08x} --- {:064b}".format(x_n, x_n, x_n))
        # print(" * random num x_a: {} --- 0x{:08x} --- {:064b}".format(x_a, x_a, x_a))

        while True:
            hash_value = get_hash_value(x_j, x_n, x_a)
            if hash_value in hash_values:
                continue
            break

        hash_values[hash_value] = True

        # print(" * hash value: {} --- 0x{:08x} --- {:064b}".format(hash_value, hash_value, hash_value))

        s1 = string_to_weekset(threads_jour[x_j])
        s2 = string_to_weekset(threads_nuit[x_n])
        s3 = string_to_weekset(threads_alt[x_a])
        # print(" * s1: {}".format(s1))
        # print(" * s2: {}".format(s2))
        # print(" * s3: {}".format(s3))

        checking(s1, s2, s3)
