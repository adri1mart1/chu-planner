import itertools
import statistics
import random
from collections import Counter
import os

# global variables
# all mathematical possible week variants
ampwv = set()
# all mathematical possible 2-weeks variants base on 1-week units
amp2wv = set()
# all mathematical possible 4-weeks variants based on 2-weeks units
amp4wv = set()
# all mathematical possible 8-weeks variants based on 4-weeks units
amp8wv = set()
# all mathematical possible 12-weeks variants based on 8-weeks units
amp12wv = set()
# all mathematical possible 16-weeks variants based on 8-weeks units
amp16wv = set()
# all mathematical possible 20-weeks variants based on 16-weeks + 4-weeks units
amp20wv = set()
week_variants = set()

min_nb_working_days_per_week = 2
max_nb_working_days_per_week = 4

'''
each month, we may work between 11 and 13 days which is
11 x 12 = 132 hours and 13 x 12 = 156 hours
A standard contract is 37.5 hours per week. With 12 hours working days
shift, that 3 days of 12 hours, 36 hours of work per week.
1,5 hour is missing so 12 hours / 1,5 hours = 8.
Every 8 weeks, an extra days of work must be worked to have a perfect
balance with 37,5 hours of work per week.
Ex: 8 week schedule: 7 weeks of 3 working days + 1 week of 4 working days
7 x 3 + 4 = 25 workings days, 25 x 12 hours = 300 hours.
300 hours / 37,5 = 8 weeks.

When combining 4-weeks units together, we need to aim for 25 days of work
exactly, hence, only one possibility exist which is combining a month of
12 days of work with a month of 13 days of work (and vice versa)
Considering 11 + 14 makes a too huge difference.
'''
min_nb_working_days_per_month = 11
min_nb_working_days_per_2months = 24
max_nb_working_days_per_month = 14
max_nb_working_days_per_2months = 26

max_nb_of_weekend_worked_per_2_months = 3


results_dir = "output"
variant_dir = os.path.join(results_dir, "variants_12w")
w1_text_file = os.path.join(variant_dir, "1-week.txt")
w1_all_text_file = os.path.join(variant_dir, "1-week.txt-all-variants.txt")
w2_text_file = os.path.join(variant_dir, "2-weeks.txt")
w2_all_text_file = os.path.join(variant_dir, "2-weeks-all-variants.txt")
w4_text_file = os.path.join(variant_dir, "4-weeks.txt")
w4_all_text_file = os.path.join(variant_dir, "4-weeks-all-variants.txt")
w8_text_file = os.path.join(variant_dir, "8-weeks.txt")
w8_all_text_file = os.path.join(variant_dir, "8-weeks-all-variants.txt")
w12_text_file = os.path.join(variant_dir, "12-weeks.txt")
w12_all_text_file = os.path.join(variant_dir, "12-weeks-all-variants.txt")
w16_text_file = os.path.join(variant_dir, "16-weeks.txt")
w20_text_file = os.path.join(variant_dir, "20-weeks.txt")


# stats variables
stats_more_than_3_consecutive_working_days = 0
stats_more_than_3_consecutive_working_days_used = False
stats_more_than_4_days_per_week = 0
stats_more_than_4_days_per_week_used = False
stats_saturday_nor_sunday = 0
stats_saturday_nor_sunday_used = False
stats_not_enough_days_off_before_or_after_working_days = 0
stats_not_enough_days_off_before_or_after_working_days_used = False
stats_too_many_single_working_days = 0
stats_too_many_single_working_days_used = False
stats_more_than_4_working_days_over_7_moving_days = 0
stats_more_than_4_working_days_over_7_moving_days_used = False
stats_two_working_week_ends_in_a_row = 0
stats_two_working_week_ends_in_a_row_used = False
stats_not_enough_or_too_many_working_days_over_n_weeks = 0
stats_not_enough_or_too_many_working_days_over_n_weeks_used = False
stats_not_exactly_1_out_of_3_working_weekend = 0
stats_not_exactly_1_out_of_3_working_weekend_used = False
stats_more_than_one_3_working_days_in_a_row = 0
stats_more_than_one_3_working_days_in_a_row_used = False


def reset_pruning_stats():
    global stats_more_than_3_consecutive_working_days
    global stats_more_than_3_consecutive_working_days_used
    global stats_more_than_4_days_per_week
    global stats_more_than_4_days_per_week_used
    global stats_saturday_nor_sunday
    global stats_saturday_nor_sunday_used
    global stats_not_enough_days_off_before_or_after_working_days
    global stats_not_enough_days_off_before_or_after_working_days_used
    global stats_too_many_single_working_days
    global stats_too_many_single_working_days_used
    global stats_more_than_4_working_days_over_7_moving_days
    global stats_more_than_4_working_days_over_7_moving_days_used
    global stats_two_working_week_ends_in_a_row
    global stats_two_working_week_ends_in_a_row_used
    global stats_not_enough_or_too_many_working_days_over_n_weeks
    global stats_not_enough_or_too_many_working_days_over_n_weeks_used
    global stats_not_exactly_1_out_of_3_working_weekend
    global stats_not_exactly_1_out_of_3_working_weekend_used
    global stats_more_than_one_3_working_days_in_a_row
    global stats_more_than_one_3_working_days_in_a_row_used
    print("reset pruning stats")
    stats_more_than_3_consecutive_working_days = 0
    stats_more_than_3_consecutive_working_days_used = False
    stats_more_than_4_days_per_week = 0
    stats_more_than_4_days_per_week_used = False
    stats_saturday_nor_sunday = 0
    stats_saturday_nor_sunday_used = False
    stats_not_enough_days_off_before_or_after_working_days = 0
    stats_not_enough_days_off_before_or_after_working_days_used = False
    stats_too_many_single_working_days = 0
    stats_too_many_single_working_days_used = False
    stats_more_than_4_working_days_over_7_moving_days = 0
    stats_more_than_4_working_days_over_7_moving_days_used = False
    stats_two_working_week_ends_in_a_row = 0
    stats_two_working_week_ends_in_a_row_used = False
    stats_not_enough_or_too_many_working_days_over_n_weeks = 0
    stats_not_enough_or_too_many_working_days_over_n_weeks_used = False
    stats_not_exactly_1_out_of_3_working_weekend = 0
    stats_not_exactly_1_out_of_3_working_weekend_used = False
    stats_more_than_one_3_working_days_in_a_row = 0
    stats_more_than_one_3_working_days_in_a_row_used = False


def print_pruning_stats():
    global stats_more_than_3_consecutive_working_days
    global stats_more_than_4_days_per_week
    global stats_saturday_nor_sunday
    global stats_not_enough_days_off_before_or_after_working_days
    global stats_too_many_single_working_days
    global stats_more_than_4_working_days_over_7_moving_days
    global stats_two_working_week_ends_in_a_row
    global stats_not_enough_or_too_many_working_days_over_n_weeks
    global stats_not_exactly_1_out_of_3_working_weekend
    global stats_more_than_one_3_working_days_in_a_row
    if stats_more_than_3_consecutive_working_days_used:
        print("stats_more_than_3_consecutive_working_days: {}".format(stats_more_than_3_consecutive_working_days))
    if stats_more_than_4_days_per_week_used:
        print("stats_more_than_4_days_per_week: {}".format(stats_more_than_4_days_per_week))
    if stats_saturday_nor_sunday_used:
        print("stats_saturday_nor_sunday: {}".format(stats_saturday_nor_sunday))
    if stats_not_enough_days_off_before_or_after_working_days_used:
        print("stats_not_enough_days_off_before_or_after_working_days: {}".format(stats_not_enough_days_off_before_or_after_working_days))
    if stats_too_many_single_working_days_used:
        print("stats_too_many_single_working_days: {}".format(stats_too_many_single_working_days))
    if stats_more_than_4_working_days_over_7_moving_days_used:
        print("stats_more_than_4_working_days_over_7_moving_days: {}".format(stats_more_than_4_working_days_over_7_moving_days))
    if stats_two_working_week_ends_in_a_row_used:
        print("stats_two_working_week_ends_in_a_row: {}".format(stats_two_working_week_ends_in_a_row))
    if stats_not_enough_or_too_many_working_days_over_n_weeks_used:
        print("stats_not_enough_or_too_many_working_days_over_n_weeks: {}".format(stats_not_enough_or_too_many_working_days_over_n_weeks))
    if stats_not_exactly_1_out_of_3_working_weekend_used:
        print("stats_not_exactly_1_out_of_3_working_weekend: {}".format(stats_not_exactly_1_out_of_3_working_weekend))
    if stats_more_than_one_3_working_days_in_a_row_used:
        print("stats_more_than_one_3_working_days_in_a_row: {}".format(stats_more_than_one_3_working_days_in_a_row))


def printw(s):
    assert(len(s)%7 == 0)
    nb_w = int(len(s)/7)
    print()
    # to enable line print header, override nb_w to 1
    # for i in range(0, nb_w):
    for i in range(0, 1):
        print("L M M J V S D ", end='')
    print()
    for i in range(0, nb_w):
        for j in range(0, 7):
        #for e in s:
            print("{} ".format(s[j+7*i]), end='')
        print()
    print("days worked: {}".format(s.count('J')))


def pruning(wset, to_del):
    print("pruning {} variants".format(len(to_del)))
    for d in to_del:
        # print("remove set {}".format(d))
        wset.discard(d)


def save_wset_to_file(wset, filename, addcount=False):
    print("Saving wset to {}".format(filename))
    with open(filename, "a") as out:
        i = 1
        for s in wset:
            if addcount:
                out.write("{} {}".format(i, ''.join(s)))
            else:
                out.write(''.join(s))
            out.write('\n')
            i = i + 1


def string_to_weekset(s):
    return tuple(s.rstrip())


def weekset_to_string(s):
    return ''.join(s)


def load_wset_from_file(filename):
    print("Loading wset from {}".format(filename))
    r = []
    with open(filename) as file:
        for line in file:
            #  print(line)
            r.append(tuple(line.rstrip()))
    return set(r)


def count_subtuple_in_tuple(b, a):
    r = 0
    for i in range(len(b)-len(a)+1):
        r += 1 if a == b[i:len(a) + i] else 0
    return r


def generate_all_mathematical_possible_week_variants():
    print("generate_all_mathematical_possible_week_variants")
    # global ampwv
    ampwv = set(itertools.permutations("".join("o" * 7 + "J" * 7), 7))
    # print("number of 1-week time possibilities before pruning {}".format(len(ampwv)))
    assert(len(ampwv) == 128)
    with open(w1_all_text_file, 'w') as out:
        for s in ampwv:
            out.write(weekset_to_string(s) + '\n')


def set_has_more_than_4_days_per_week(s) -> bool:
    global stats_more_than_4_days_per_week
    global stats_more_than_4_days_per_week_used
    stats_more_than_4_days_per_week_used = True
    if s.count('J') > 4:
        stats_more_than_4_days_per_week += 1
        return True
    return False


def set_has_more_than_3_consecutive_working_days(s) -> bool:
    global stats_more_than_3_consecutive_working_days
    global stats_more_than_3_consecutive_working_days_used
    stats_more_than_3_consecutive_working_days_used = True
    p = ('J', 'J', 'J', 'J')
    if any(p == s[i:len(p) + i] for i in range(len(s) - len(p) + 1)):
        stats_more_than_3_consecutive_working_days += 1
        return True
    return False


def set_has_saturday_nor_sunday(s) -> bool:
    """ remove from variants if saturday is a working day and sunday is
        not and vice versa """
    global stats_saturday_nor_sunday
    global stats_saturday_nor_sunday_used
    stats_saturday_nor_sunday_used = True
    assert(len(s) == 7)
    if s[-1] != s[-2]:
        stats_saturday_nor_sunday += 1
        return True
    return False


def set_has_not_enough_days_off_before_or_after_working_days(s) -> bool:
    """ remove all variants which do not respect 2 days off after
        2 or 3 working days """
    global stats_not_enough_days_off_before_or_after_working_days
    global stats_not_enough_days_off_before_or_after_working_days_used
    stats_not_enough_days_off_before_or_after_working_days_used = True
    a = ('J', 'J', 'o', 'J')
    b = ('J', 'J', 'J', 'o', 'J')
    c = ('J', 'o', 'J', 'J', 'J')
    if (any(a == s[i:len(a) + i] for i in range(len(s) - len(a) + 1))) or \
       (any(b == s[i:len(b) + i] for i in range(len(s) - len(b) + 1))) or \
       (any(c == s[i:len(c) + i] for i in range(len(s) - len(c) + 1))):
        stats_not_enough_days_off_before_or_after_working_days += 1
        return True
    return False


def set_has_too_many_single_working_days(s) -> bool:
    global stats_too_many_single_working_days
    global stats_too_many_single_working_days_used
    stats_too_many_single_working_days_used = True
    a = ('J', 'o', 'J', 'o', 'J')
    if (any(a == s[i:len(a) + i] for i in range(len(s) - len(a) + 1))):
        stats_too_many_single_working_days += 1
        return True
    return False


def assemble_variants_two_by_two(out_weeklen, input_file_1, weeklen_file_1, input_file_2, weeklen_file_2, output_file):
    print("assemble_variants_two_by_two")
    size_file_1 = os.stat(input_file_1).st_size
    size_file_2 = os.stat(input_file_2).st_size
    n_lines_file_1 = int(size_file_1 / (weeklen_file_1*7+1))
    n_lines_file_2 = int(size_file_2 / (weeklen_file_2*7+1))
    max_disk_usage = 10000000 # 10Mb
    n_frames_to_keep = int(max_disk_usage / (out_weeklen*7+1))
    to_be_generated = n_lines_file_1 * n_lines_file_2
    skip_cnt = round(to_be_generated / n_frames_to_keep)
    if to_be_generated > n_frames_to_keep:
        print("input_file 1 size {} bytes which represents {} variants".format(size_file_1, n_lines_file_1))
        print("input_file 2 size {} bytes which represents {} variants".format(size_file_2, n_lines_file_2))
        print("We must limit disk usage to {} bytes with frame generation of {} chars each".format(max_disk_usage, out_weeklen*7+1))
        print("total number of possibilities {} x {} = {}".format(n_lines_file_1, n_lines_file_2, to_be_generated))
        print("Number of {}-weeks variants to keep to respect disk usage: {}".format(out_weeklen, n_frames_to_keep))

    cnt = 0
    sk_cnt = 0
    with open(output_file, 'w') as out:
        with open(input_file_1) as f1:
            for l1 in f1:
                s1 = string_to_weekset(l1)
                with open(input_file_2) as f2:
                    for l2 in f2:
                        if sk_cnt > skip_cnt:
                            sk_cnt = 0
                            s2 = string_to_weekset(l2)
                            ns = tuple(s1 + s2)
                            out.write(weekset_to_string(ns) + '\n')
                            cnt = cnt + 1
                        sk_cnt +=1
    print("total number of {}-weeks time possibilities before pruning {}".format(out_weeklen, cnt))


def set_has_more_than_4_working_days_over_7_moving_days(s):
    global stats_more_than_4_working_days_over_7_moving_days
    global stats_more_than_4_working_days_over_7_moving_days_used
    stats_more_than_4_working_days_over_7_moving_days_used = True
    assert(len(s) >= 7)
    for i in range(0, len(s)-7):
        ss = tuple(s[i:7+i])
        if ss.count('J') > 4:
            stats_more_than_4_working_days_over_7_moving_days += 1
            return True
    return False


def set_has_two_working_week_ends_in_a_row(s) -> bool:
    global stats_two_working_week_ends_in_a_row
    global stats_two_working_week_ends_in_a_row_used
    stats_two_working_week_ends_in_a_row_used = True
    assert((len(s) % 7) == 0)
    assert(len(s) > 0)
    n_w = int(len(s)/7)
    prev = ""
    for i in range(0, n_w):
        if prev == s[7*i+6] and prev == 'J':
            stats_two_working_week_ends_in_a_row += 1
            return True
        prev = s[7*i+6]
    return False


def remove_if_working_days_not_well_balanced_during_the_week(wset):
    print("remove_if_working_days_not_well_balanced_during_the_week")
    n_w = int(len(next(iter(wset)))/7)
    res = []
    for s in wset:
        dc = dict()
        dc["set"] = s
        # print("s: {}".format(s))
        nb_d = [0]*5
        for w in range(0, n_w):
            for d in range(0, 5):
                nb_d[d] += 1 if s[7*w+d] == 'J' else 0
        sd = statistics.stdev(nb_d)
        dc["stdev"] = sd
        # print(nb_d)
        dc["nb_d"] = nb_d
        res.append(dc)

    cnt = Counter(z["stdev"] for z in res)
    cnt = sorted(cnt.items())
    n = 2
    print("keeping all {} best balanced".format(n))
    best_stdev = []
    for e in cnt:
        if len(best_stdev) < n:
            print("standard deviation: {} number of items concerned: {}".format(e[0], e[1]))
            best_stdev.append(e)
        else:
            break

    to_del = []
    for r in res:
        if r["stdev"] > best_stdev[-1][0]:
            #print("remove set -> {} - {}:".format(r["stdev"], r["nb_d"]))
            #printw(r["set"])
            to_del.append(r["set"])
        # else:
        #     print("keeping set -> {} - {}:".format(r["stdev"], r["nb_d"]))
        #     printw(r["set"])
    pruning(wset, to_del)


def set_has_not_enough_or_too_many_working_days_over_n_weeks(s, mini, maxi) -> bool:
    global stats_not_enough_or_too_many_working_days_over_n_weeks
    global stats_not_enough_or_too_many_working_days_over_n_weeks_used
    stats_not_enough_or_too_many_working_days_over_n_weeks_used = True
    c = s.count('J')
    if c < mini or c > maxi:
        stats_not_enough_or_too_many_working_days_over_n_weeks += 1
        return True
    return False


def set_has_more_than_one_3_working_days_in_a_row(s):
    global stats_more_than_one_3_working_days_in_a_row
    global stats_more_than_one_3_working_days_in_a_row_used
    stats_more_than_one_3_working_days_in_a_row_used = True
    a = ('J', 'J', 'J')
    if count_subtuple_in_tuple(s, a) > 1:
        stats_more_than_one_3_working_days_in_a_row += 1
        return True
    return False


def remove_if_no_free_frisatsun_per_month(wset):
    print("remove_if_no_free_frisatsun_per_month")
    n_w = int(len(next(iter(wset)))/7)
    to_del = []
    for s in wset:
        found = False
        for i in range(0, n_w):
            if s[4+7*i] == 'o' and s[5+7*i] == 'o' and s[6+7*i] == 'o':
                found = True
                break
        if not found:
            to_del.append(s)
    pruning(wset, to_del)


def remove_if_too_many_working_weekends_over_2months(wset):
    print("remove_if_too_many_working_weekends_over_2months")
    n_w = int(len(next(iter(wset)))/7)
    to_del = []
    for s in wset:
        r = 0
        for i in range(n_w):
            r += 1 if s[6+7*i] == 'J' else 0
        if r > max_nb_of_weekend_worked_per_2_months:
            to_del.append(s)
    pruning(wset, to_del)


def remove_if_more_than_one_single_free_weekend_over_2months(wset):
    print("remove_if_more_than_one_single_free_weekend_over_2months")
    n_w = int(len(next(iter(wset)))/7)
    to_del = []
    for s in wset:
        cnt = 0
        for i in range(0, n_w-3):
            if s[6+7*i] == 'J' and s[6+7*(i+1)] == 'o' and s[6+7*(i+2)] == 'J':
                cnt = cnt + 1
        if cnt > 1:
            to_del.append(s)
    pruning(wset, to_del)


def set_has_not_exactly_1_out_of_3_working_weekend(s) -> bool:
    global stats_not_exactly_1_out_of_3_working_weekend
    global stats_not_exactly_1_out_of_3_working_weekend_used
    stats_not_exactly_1_out_of_3_working_weekend_used = True
    assert(len(s) > 27) # we need a month to call this function
    assert((len(s) % 7) == 0)
    n_w = int(len(s)/7)
    n_iter = int(n_w / 3)
    n_iter += 1 if (n_w % 3) != 0 else 0
    w1 = s[6]
    w2 = s[6+7]
    w3 = s[6+14]
    if tuple(w1+w2+w3).count('J') != 1:
        return True
    for i in range(1, n_iter):
        idx = 6+7*(3*i)
        if idx < len(s) and s[idx] != w1:
            stats_not_exactly_1_out_of_3_working_weekend += 1
            return True
        idx += 7
        if idx < len(s):
            if s[idx] != w2:
                stats_not_exactly_1_out_of_3_working_weekend += 1
                return True
        idx += 7
        if idx < len(s):
            if s[idx] != w3:
                stats_not_exactly_1_out_of_3_working_weekend += 1
                return True
    return False


def filter_all_impossible_week_variants():
    print("filter_all_impossible_week_variants")
    cnt = 0
    with open(w1_text_file, 'w') as out:
        with open(w1_all_text_file) as f:
            for line in f:
                s = string_to_weekset(line)

                if set_has_more_than_3_consecutive_working_days(s):
                    continue

                if set_has_more_than_4_days_per_week(s):
                    continue

                if set_has_saturday_nor_sunday(s):
                    continue

                if set_has_not_enough_days_off_before_or_after_working_days(s):
                    continue

                if set_has_too_many_single_working_days(s):
                    continue

                out.write(weekset_to_string(s) + '\n')
                cnt = cnt + 1

    print_pruning_stats()
    reset_pruning_stats()
    print("all valid week variants size:{}\n".format(cnt))


def filter_all_impossible_two_weeks_variants():
    print("filter_all_impossible_two_weeks_variants")
    cnt = 0
    with open(w2_text_file, 'w') as out:
        with open(w2_all_text_file) as f:
            for line in f:
                s = string_to_weekset(line)

                if set_has_more_than_3_consecutive_working_days(s):
                    continue

                if set_has_not_enough_days_off_before_or_after_working_days(s):
                    continue

                if set_has_more_than_4_working_days_over_7_moving_days(s):
                    continue

                if set_has_two_working_week_ends_in_a_row(s):
                    continue

                if set_has_not_enough_or_too_many_working_days_over_n_weeks(s, min_nb_working_days_per_week*2, max_nb_working_days_per_week*2):
                    continue

                if set_has_too_many_single_working_days(s):
                    continue

                out.write(weekset_to_string(s) + '\n')
                cnt = cnt + 1

    print_pruning_stats()
    reset_pruning_stats()
    print("all valid 2-weeks variants size: {}\n".format(cnt))


def filter_all_impossible_four_weeks_variants():
    print("filter_all_impossible_four_weeks_variants")
    cnt = 0
    with open(w4_text_file, 'w') as out:
        with open(w4_all_text_file) as f:
            for line in f:
                s = string_to_weekset(line)

                # seems the well balanced function is too strict to work well on 4 weeks
                # remove_if_working_days_not_well_balanced_during_the_week(amp4wv)

                if set_has_not_exactly_1_out_of_3_working_weekend(s):
                    continue

                if set_has_more_than_one_3_working_days_in_a_row(s):
                    continue

                if set_has_more_than_3_consecutive_working_days(s):
                    continue

                if set_has_not_enough_or_too_many_working_days_over_n_weeks(s, min_nb_working_days_per_month, max_nb_working_days_per_month):
                    continue

                if set_has_not_enough_days_off_before_or_after_working_days(s):
                    continue

                if set_has_more_than_4_working_days_over_7_moving_days(s):
                    continue

                if set_has_two_working_week_ends_in_a_row(s):
                    continue

                # remove_if_not_6_workings_days_over_two_weeks_period(amp4wv)

                if set_has_too_many_single_working_days(s):
                    continue

                # # optional pruning
                # remove_if_more_than_one_3_working_days_in_a_row_per_month(amp4wv)
                # remove_if_no_free_frisatsun_per_month(amp4wv)

                out.write(weekset_to_string(s) + '\n')
                cnt = cnt + 1

    print_pruning_stats()
    reset_pruning_stats()
    print("all valid 4-weeks variants size after balance pruning: {}\n".format(cnt))


def filter_all_impossible_eight_weeks_variants():
    print("filter_all_impossible_eight_weeks_variants")
    cnt = 0
    with open(w8_text_file, 'w') as out:
        with open(w8_all_text_file) as f:
            for line in f:
                s = string_to_weekset(line)

                if set_has_not_exactly_1_out_of_3_working_weekend(s):
                    continue

                if set_has_more_than_one_3_working_days_in_a_row(s):
                    continue

                # if set_has_not_enough_or_too_many_working_days_over_n_weeks(s, min_nb_working_days_per_2months, max_nb_working_days_per_2months):
                #     continue

                if set_has_more_than_3_consecutive_working_days(s):
                    continue

                if set_has_not_enough_days_off_before_or_after_working_days(s):
                    continue

                if set_has_more_than_4_working_days_over_7_moving_days(s):
                    continue

                if set_has_two_working_week_ends_in_a_row(s):
                    continue

                # # optional pruning
                # remove_if_working_days_not_well_balanced_during_the_week(amp8wv)
                # remove_if_more_than_one_3_working_days_in_a_row_per_month(amp8wv)
                # remove_if_too_many_working_weekends_over_2months(amp8wv)
                # remove_if_too_many_single_working_days(amp8wv)
                # remove_if_more_than_one_single_free_weekend_over_2months(amp8wv)

                out.write(weekset_to_string(s) + '\n')
                cnt = cnt + 1

    print_pruning_stats()
    reset_pruning_stats()
    print("all valid 8-weeks variants size: {}\n".format(cnt))


def filter_all_impossible_twelve_weeks_variants():
    print("filter_all_impossible_twelve_weeks_variants")
    cnt = 0
    with open(w12_text_file, 'w') as out:
        with open(w12_all_text_file) as f:
            for line in f:
                s = string_to_weekset(line)

                if set_has_not_exactly_1_out_of_3_working_weekend(s):
                    continue

                if set_has_more_than_one_3_working_days_in_a_row(s):
                    continue

                if set_has_more_than_3_consecutive_working_days(s):
                    continue

                if set_has_not_enough_days_off_before_or_after_working_days(s):
                    continue

                if set_has_more_than_4_working_days_over_7_moving_days(s):
                    continue

                if set_has_two_working_week_ends_in_a_row(s):
                    continue

                # check rotation by creating subset
                l = int(len(s) / 2)
                ss = tuple(s[-l:] + s[:l])

                if set_has_not_exactly_1_out_of_3_working_weekend(ss):
                    continue

                if set_has_more_than_3_consecutive_working_days(ss):
                    continue

                if set_has_not_enough_days_off_before_or_after_working_days(ss):
                    continue

                if set_has_more_than_4_working_days_over_7_moving_days(ss):
                    continue

                if set_has_two_working_week_ends_in_a_row(ss):
                    continue

                out.write(weekset_to_string(s) + '\n')
                cnt = cnt + 1

    print_pruning_stats()
    reset_pruning_stats()
    print("all valid 12-weeks variants size: {}\n".format(cnt))


if __name__ == "__main__":

    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(variant_dir, exist_ok=True)

    # 1 week part
    if not os.path.isfile(w1_text_file):
        generate_all_mathematical_possible_week_variants()
        filter_all_impossible_week_variants()
    else:
        print("file {} already exists, using it".format(w1_text_file))

    # 2 weeks part
    if not os.path.isfile(w2_all_text_file):
        assemble_variants_two_by_two(2, w1_text_file, 1, w1_text_file, 1, w2_all_text_file)
    if not os.path.isfile(w2_text_file):
        filter_all_impossible_two_weeks_variants()
    else:
        print("file {} already exists, using it".format(w2_text_file))

    # 4 weeks part
    if not os.path.isfile(w4_all_text_file):
        assemble_variants_two_by_two(4, w2_text_file, 2, w2_text_file, 2, w4_all_text_file)
    if not os.path.isfile(w4_text_file):
        filter_all_impossible_four_weeks_variants()
    else:
        print("file {} already exists, using it".format(w4_text_file))

    # 8 weeks part
    if not os.path.isfile(w8_all_text_file):
        assemble_variants_two_by_two(8, w4_text_file, 4, w4_text_file, 4, w8_all_text_file)
    if not os.path.isfile(w8_text_file):
        filter_all_impossible_eight_weeks_variants()
    else:
        print("file {} already exists, using it".format(w8_text_file))

    # 12 weeks parts
    if not os.path.isfile(w12_all_text_file):
        assemble_variants_two_by_two(12, w8_text_file, 8, w4_text_file, 4, w12_all_text_file)
    if not os.path.isfile(w12_text_file):
        filter_all_impossible_twelve_weeks_variants()
    else:
        print("file {} already exists, using it".format(w12_text_file))
