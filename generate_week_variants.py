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
w2_text_file = os.path.join(variant_dir, "2-weeks.txt")
w4_text_file = os.path.join(variant_dir, "4-weeks.txt")
w8_text_file = os.path.join(variant_dir, "8-weeks.txt")
w12_text_file = os.path.join(variant_dir, "12-weeks.txt")
w16_text_file = os.path.join(variant_dir, "16-weeks.txt")
w20_text_file = os.path.join(variant_dir, "20-weeks.txt")


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
    global ampwv
    ampwv = set(itertools.permutations("".join("o" * 7 + "J" * 7), 7))
    print("number of 1-week time possibilities before pruning {}".format(len(ampwv)))
    assert(len(ampwv) == 128)


def remove_if_more_than_4_days_per_week():
    print("remove_if_more_than_4_days_per_week")
    global ampwv
    to_del = []
    for s in ampwv:
        if s.count('J') > 4:
            to_del.append(s)
    pruning(ampwv, to_del)


def remove_if_more_than_3_consecutive_working_days(wset):
    print("remove_if_more_than_3_consecutive_working_days")
    to_del = []
    p = ('J', 'J', 'J', 'J')
    for s in wset:
        if any(p == s[i:len(p) + i] for i in range(len(s) - len(p) + 1)):
            to_del.append(s)
    pruning(wset, to_del)


def remove_if_saturday_nor_sunday():
    """ remove from variants if saturday is a working day and sunday is
        not and vice versa """
    print("remove_if_saturday_nor_sunday")
    global ampwv
    to_del = []
    for s in ampwv:
        if s[-1] != s[-2]:
            to_del.append(s)
    pruning(ampwv, to_del)


def remove_if_not_enough_days_off_before_or_after_working_days(wset):
    """ remove all variants which do not respect 2 days off after
        2 or 3 working days """
    print("remove_if_not_enough_days_off_before_or_after_working_days")
    to_del = []
    a = ('J', 'J', 'o', 'J')
    b = ('J', 'J', 'J', 'o', 'J')
    c = ('J', 'o', 'J', 'J', 'J')
    for s in wset:
        if (any(a == s[i:len(a) + i] for i in range(len(s) - len(a) + 1))) or \
           (any(b == s[i:len(b) + i] for i in range(len(s) - len(b) + 1))) or \
           (any(c == s[i:len(c) + i] for i in range(len(s) - len(c) + 1))):
            to_del.append(s)
    pruning(wset, to_del)


def remove_if_too_many_single_working_days(wset):
    print("remove_if_too_many_single_working_days")
    to_del = []
    a = ('J', 'o', 'J', 'o', 'J')
    for s in wset:
        if (any(a == s[i:len(a) + i] for i in range(len(s) - len(a) + 1))):
            to_del.append(s)
    pruning(wset, to_del)


def assemble_variants_on_two_weeks_time():
    print("assemble_variants_on_two_weeks_time")
    global amp2wv, ampwv
    r = []
    for s in ampwv:
        for t in ampwv:
            r.append(s + t)
    amp2wv = set(r)
    print("number of 2-weeks time possibilities before pruning {}".format(len(amp2wv)))


def assemble_variants_on_four_weeks_time():
    print("assemble_variants_on_four_weeks_time")
    global amp2wv, amp4wv
    r = []
    for a in amp2wv:
        for b in amp2wv:
            r.append(a + b)
    amp4wv = set(r)
    print("number of 4-weeks time possibilities before pruning {}".format(len(amp4wv)))


def assemble_variants_on_eight_weeks_time():
    print("assemble_variants_on_eight_weeks_time")
    global amp4wv, amp8wv
    r = []
    for a in amp4wv:
        for b in amp4wv:
            r.append(a + b)
    amp8wv = set(r)
    print("number of 8-weeks time possibilities before pruning {}".format(len(amp8wv)))


def assemble_variants_on_twelve_weeks_time():
    print("assemble_variants_on_twelve_weeks_time")
    global amp8wv, amp4wv, amp12wv
    r = []
    for a in amp8wv:
        for b in amp4wv:
            r.append(a + b)
    amp12wv = set(r)
    print("number of 12-weeks time possibilities before pruning {}".format(len(amp12wv)))


def assemble_variants_on_sixteen_weeks_time():
    print("assemble_variants_on_sixteen_weeks_time")
    global amp8wv, amp16wv
    r = []
    for a in amp8wv:
        for b in amp8wv:
            r.append(a + b)
    amp16wv = set(r)
    print("number of 16-weeks time possibilities before pruning {}".format(len(amp16wv)))


def assemble_variants_on_twenty_weeks_time():
    print("assemble_variants_on_twenty_weeks_time")
    global amp16wv, amp20wv, amp4wv
    r = []
    for a in amp16wv:
        for b in amp4wv:
            r.append(a + b)
    amp20wv = set(r)
    print("number of 20-weeks time possibilities before pruning {}".format(len(amp20wv)))


def remove_if_more_than_4_working_days_over_7_moving_days(wset):
    print("remove_if_more_than_4_working_days_over_7_moving_days")
    to_del = []
    for s in wset:
        for i in range(0, len(s)-7):
            ss = tuple(s[i:7+i])
            if ss.count('J') > 4:
                to_del.append(s)
    pruning(wset, to_del)


def remove_if_two_working_week_ends_in_a_row(wset):
    print("remove_if_two_working_week_ends_in_a_row")
    n_w = int(len(next(iter(wset)))/7)
    to_del = []
    for s in wset:
        prev = ""
        for i in range(0, n_w):
            if prev == s[7*i+6] and prev == 'J':
                to_del.append(s)
                break
            prev = s[7*i+6]
    pruning(wset, to_del)


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


def remove_if_not_enough_or_too_many_working_days_over_n_weeks(wset, mini, maxi):
    print("remove_if_not_enough_or_too_many_working_days_over_a_month -> min:{} max:{} days".format(mini, maxi))
    to_del = []
    for s in wset:
        c = s.count('J')
        if c < mini or c > maxi:
            to_del.append(s)
    pruning(wset, to_del)


def remove_if_more_than_one_3_working_days_in_a_row_per_month(wset):
    print("remove_if_more_than_one_3_working_days_in_a_row_per_month")
    a = ('J', 'J', 'J')
    to_del = []
    for s in wset:
        if count_subtuple_in_tuple(s, a) > 1:
            to_del.append(s)
    pruning(wset, to_del)


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


def remove_if_not_exactly_1_out_of_3_working_weekend(wset):
    print("remove_if_not_exactly_1_out_of_3_working_weekend")
    n_w = int(len(next(iter(wset)))/7)
    to_del = []
    a = ('J', 'o', 'o', 'J', 'o', 'o', 'J', 'o', 'o', 'J', 'o', 'o')
    b = ('o', 'J', 'o', 'o', 'J', 'o', 'o', 'J', 'o', 'o', 'J', 'o')
    c = ('o', 'o', 'J', 'o', 'o', 'J', 'o', 'o', 'J', 'o', 'o', 'J')
    for s in wset:
        # printw(s)
        weekends = []
        for n in range(0, n_w):
            weekends.append(s[6+n*7])
        w_set = set(weekends)
        if w_set != a and w_set != b and w_set != c:
            # print("invalid")
            # printw(s)
            to_del.append(s)
        else:
            print("valid")
            printw(s)
    pruning(wset, to_del)


# def remove_if_variant_rotation_is_impossible(wset):
#     print("remove_if_variant_rotation_is_impossible")
#     """ a variant is only valid if the continuous rotation is possible. """
#     to_del = []
#     p = ('J', 'J', 'J', 'J')
#     for s in wset:
#         print("set:    {}".format(s))
#         ss = tuple(b[-7:]+b[:7])
#         print("subset: {}".format(ss))
#         # detect too many working days in a row
#         if any(p == ss[i:len(p) + i] for i in range(len(ss) - len(p) + 1)):
#             to_del.append(s)
#     pruning(wset, to_del)
#     exit(0)

def filter_all_impossible_week_variants():
    print("filter_all_impossible_week_variants")
    global ampwv
    remove_if_more_than_4_days_per_week()
    remove_if_more_than_3_consecutive_working_days(ampwv)
    remove_if_saturday_nor_sunday()
    remove_if_not_enough_days_off_before_or_after_working_days(ampwv)
    remove_if_too_many_single_working_days(ampwv)
    print("all valid week variants size:{}\n".format(len(ampwv)))


def filter_all_impossible_two_weeks_variants():
    print("filter_all_impossible_two_weeks_variants")
    global amp2wv
    remove_if_more_than_3_consecutive_working_days(amp2wv)
    remove_if_not_enough_days_off_before_or_after_working_days(amp2wv)
    remove_if_more_than_4_working_days_over_7_moving_days(amp2wv)
    remove_if_two_working_week_ends_in_a_row(amp2wv)
    remove_if_not_enough_or_too_many_working_days_over_n_weeks(
        amp2wv, min_nb_working_days_per_week*2, max_nb_working_days_per_week*2)
    remove_if_too_many_single_working_days(amp2wv)
    print("all valid 2-weeks variants size: {}\n".format(len(amp2wv)))


def filter_all_impossible_four_weeks_variants():
    print("filter_all_impossible_four_weeks_variants")
    global amp4wv
    # seems the well balanced function is too strict to work well on 4 weeks
    # remove_if_working_days_not_well_balanced_during_the_week(amp4wv)
    remove_if_not_enough_or_too_many_working_days_over_n_weeks(
        amp4wv, min_nb_working_days_per_month, max_nb_working_days_per_month)
    remove_if_more_than_3_consecutive_working_days(amp4wv)
    remove_if_not_enough_days_off_before_or_after_working_days(amp4wv)
    remove_if_more_than_4_working_days_over_7_moving_days(amp4wv)
    remove_if_two_working_week_ends_in_a_row(amp4wv)
    # remove_if_not_6_workings_days_over_two_weeks_period(amp4wv)
    remove_if_too_many_single_working_days(amp4wv)
    print("all valid 4-weeks variants size: {}\n".format(len(amp4wv)))
    # optional pruning
    remove_if_more_than_one_3_working_days_in_a_row_per_month(amp4wv)
    remove_if_no_free_frisatsun_per_month(amp4wv)
    print("all valid 4-weeks variants size after balance pruning: {}\n".format(len(amp4wv)))


def filter_all_impossible_eight_weeks_variants():
    print("filter_all_impossible_eight_weeks_variants")
    global amp8wv
    remove_if_not_enough_or_too_many_working_days_over_n_weeks(
        amp8wv, min_nb_working_days_per_2months, max_nb_working_days_per_2months)
    remove_if_more_than_3_consecutive_working_days(amp8wv)
    remove_if_not_enough_days_off_before_or_after_working_days(amp8wv)
    remove_if_more_than_4_working_days_over_7_moving_days(amp8wv)
    remove_if_two_working_week_ends_in_a_row(amp8wv)
    print("all valid 8-weeks variants size: {}\n".format(len(amp8wv)))
    # optional pruning
    remove_if_working_days_not_well_balanced_during_the_week(amp8wv)
    remove_if_more_than_one_3_working_days_in_a_row_per_month(amp8wv)
    remove_if_too_many_working_weekends_over_2months(amp8wv)
    remove_if_too_many_single_working_days(amp8wv)
    remove_if_more_than_one_single_free_weekend_over_2months(amp8wv)


def filter_all_impossible_twelve_weeks_variants():
    print("filter_all_impossible_twelve_weeks_variants")
    remove_if_not_exactly_1_out_of_3_working_weekend(amp12wv)
    remove_if_more_than_3_consecutive_working_days(amp12wv)
    remove_if_not_enough_days_off_before_or_after_working_days(amp12wv)
    remove_if_more_than_4_working_days_over_7_moving_days(amp12wv)
    remove_if_two_working_week_ends_in_a_row(amp12wv)


def filter_all_impossible_sixteen_weeks_variants():
    print("filter_all_impossible_sixteen_weeks_variants")
    remove_if_more_than_3_consecutive_working_days(amp16wv)
    remove_if_not_enough_days_off_before_or_after_working_days(amp16wv)
    remove_if_more_than_4_working_days_over_7_moving_days(amp16wv)
    remove_if_two_working_week_ends_in_a_row(amp16wv)
    print("all valid 16-weeks variants size: {}\n".format(len(amp16wv)))


def filter_all_impossible_twenty_weeks_variants():
    print("filter_all_impossible_twenty_weeks_variants")
    # remove_if_variant_rotation_is_impossible(amp20wv)
    remove_if_more_than_3_consecutive_working_days(amp20wv)
    remove_if_not_enough_days_off_before_or_after_working_days(amp20wv)
    remove_if_more_than_4_working_days_over_7_moving_days(amp20wv)
    remove_if_two_working_week_ends_in_a_row(amp20wv)
    print("all valid 20-weeks variants size: {}\n".format(len(amp20wv)))


def filter_all_impossible_rotation_week_variants(wset):
    print("filter_all_impossible_rotation_week_variants")
    p = ('J', 'J', 'J', 'J')
    to_del = []
    print("remove if too many working days worked")
    for s in wset:
        # concatenate last week and first week and check if rotation is valid
        ss = tuple(s[-7:] + s[0:7])
        if any(p == ss[i:len(p) + i] for i in range(len(ss) - len(p) + 1)):
            to_del.append(s)

    pruning(wset, to_del)
    to_del.clear()

    print("remove_if_not_enough_days_off_before_or_after_working_days")
    a = ('J', 'J', 'o', 'J')
    b = ('J', 'J', 'J', 'o', 'J')
    c = ('J', 'o', 'J', 'J', 'J')
    for s in wset:
        ss = tuple(s[-7:] + s[0:7])
        if (any(a == ss[i:len(a) + i] for i in range(len(ss) - len(a) + 1))) or \
           (any(b == ss[i:len(b) + i] for i in range(len(ss) - len(b) + 1))) or \
           (any(c == ss[i:len(c) + i] for i in range(len(ss) - len(c) + 1))):
            to_del.append(s)
    pruning(wset, to_del)
    to_del.clear()

    print("remove_if_more_than_4_working_days_over_7_moving_days")
    for s in wset:
        ss = tuple(s[-7:] + s[0:7])
        for i in range(0, len(ss)-7):
            sss = tuple(ss[i:7+i])
            if sss.count('J') > 4:
                to_del.append(s)
    pruning(wset, to_del)
    to_del.clear()

    print("all valid 20-weeks variants size: {}\n".format(len(amp20wv)))


if __name__ == "__main__":

    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(variant_dir, exist_ok=True)

    # 1 week part
    if not os.path.isfile(w1_text_file):
        generate_all_mathematical_possible_week_variants()
        filter_all_impossible_week_variants()
        save_wset_to_file(ampwv, w1_text_file)
    else:
        print("file {} already exists, using it".format(w1_text_file))
        ampwv = load_wset_from_file(w1_text_file)

    # 2 weeks part
    if not os.path.isfile(w2_text_file):
        assemble_variants_on_two_weeks_time()
        filter_all_impossible_two_weeks_variants()
        save_wset_to_file(amp2wv, w2_text_file)
    else:
        print("file {} already exists, using it".format(w2_text_file))
        amp2wv = load_wset_from_file(w2_text_file)

    # 4 weeks part
    if not os.path.isfile(w4_text_file):
        assemble_variants_on_four_weeks_time()
        filter_all_impossible_four_weeks_variants()
        save_wset_to_file(amp4wv, w4_text_file)
    else:
        print("file {} already exists, using it".format(w4_text_file))
        amp4wv = load_wset_from_file(w4_text_file)

    # 8 weeks part
    if not os.path.isfile(w8_text_file):
        if len(amp4wv) > 1000:
            print("amp4wv len is {}, taking best 1000 randomly".format(len(amp4wv)))
            amp4wv = random.sample(amp4wv, 1000)
        assemble_variants_on_eight_weeks_time()
        filter_all_impossible_eight_weeks_variants()
        save_wset_to_file(amp8wv, w8_text_file)
    else:
        print("file {} already exists, using it".format(w8_text_file))
        amp8wv = load_wset_from_file(w8_text_file)

    exit(0)

    # 12 weeks parts
    if not os.path.isfile(w12_text_file):
        if len(amp8wv) > 1000:
            print("amp8wv len is {}, taking best 1000 randomly".format(len(amp8wv)))
            amp8wv = random.sample(amp8wv, 1000)
        assemble_variants_on_twelve_weeks_time()
        filter_all_impossible_twelve_weeks_variants()
        filter_all_impossible_rotation_week_variants(amp12wv)
        save_wset_to_file(amp12wv, w12_text_file)
    else:
        print("file {} already exists, using it".format(w12_text_file))
        amp12wv = load_wset_from_file(w12_text_file)
    remove_if_not_exactly_1_out_of_3_working_weekend(amp12wv)

    # # 16 weeks part
    # if not os.path.isfile(w16_text_file):
    #     if len(amp8wv) > 2000:
    #         print("amp8wv len is {}, taking best 2000 randomly".format(len(amp8wv)))
    #         amp8wv = random.sample(amp8wv, 2000)
    #     assemble_variants_on_sixteen_weeks_time()
    #     filter_all_impossible_sixteen_weeks_variants()
    #     save_wset_to_file(amp16wv, w16_text_file)
    # else:
    #     print("file {} already exists, using it".format(w16_text_file))
    #     amp16wv = load_wset_from_file(w16_text_file)

    # # 20 weeks parts
    # if not os.path.isfile(w20_text_file):
    #     if len(amp16wv) > 2000:
    #         print("amp16wv len is {}, taking best 2000 randomly".format(len(amp16wv)))
    #         amp16wv = random.sample(amp16wv, 2000)
    #     assemble_variants_on_twenty_weeks_time()
    #     filter_all_impossible_twenty_weeks_variants()
    #     filter_all_impossible_rotation_week_variants(amp20wv)
    #     save_wset_to_file(amp20wv, w20_text_file)
    # else:
    #     print("file {} already exists, using it".format(w20_text_file))
    #     amp20wv = load_wset_from_file(w20_text_file)


    # generate w20_try file
    # amp20wv_try = random.sample(amp20wv, 1000000)
    # save_wset_to_file(amp20wv_try, "w20_variants_try.txt", addcount=True)
    # save_wset_to_file(amp20wv, "w20_variants_try.txt", addcount=True)
