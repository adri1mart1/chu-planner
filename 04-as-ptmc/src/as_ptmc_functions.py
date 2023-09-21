import sys
sys.path.append('../../00-common/src/')

from os import stat, makedirs
from os.path import join
from functions import string_to_weekset, weekset_to_string

results_dir = "../output"
variant_dir = join(results_dir, "variants_12w")
combination_dir = join(results_dir, "combinations")

makedirs(results_dir, exist_ok=True)
makedirs(variant_dir, exist_ok=True)
makedirs(combination_dir, exist_ok=True)

''' 1Mo limit per file when stored '''
max_disk_usage_per_file = 1000000

''' global min/max variables
actual working time is 37,5h per week. That means 5 days of 7,5h of work.
Over 4 weeks, it's 150h (4x37,5).
We choose to be 150h +/- 24h as it's max 2 days of 12h differences
'''
min_number_of_hours_per_month = 126
max_number_of_hours_per_month = 174


# store all 1week variant raw
all_1w_raw = []

# store all 1week variant pruned
all_1w_pruned = []


def get_number_of_hours(s) -> float:
    d = {
        'o': 0,
        'J': 12,
        'M': 7.5
    }
    return sum(d[val] for val in s)


def is_a_working_day(day):
    return day in ['J', 'M']


def is_a_rest_day(day):
    return not is_a_working_day()


def is_12h_working_day(day):
    return day == 'J'


def is_a_7h30_working_day(day):
    return day == 'M'


def printw_asptmc(s, detailed_hours=False):
    d = {
        'o': 'off',
        'J': '12h',
        'M': '7.5'
    }
    assert (len(s) % 7 == 0)
    nb_w = int(len(s) / 7)
    jours_semaine = 'Lun Mar Mer Jeu Ven Sam Dim'
    jours_semaine_formate = ' '.join([j.ljust(4) for j in jours_semaine.split()])
    print(jours_semaine_formate)
    for i in range(0, nb_w):
        for j in range(0, 7):
            print("{}".format(d[s[j + 7 * i]]).ljust(5), end='')
        print()
    if detailed_hours:
        print(" -- days:{}/{}".format(7*nb_w - s.count('z'), len(s)), end='')
        print(" hours: {}h".format(get_number_of_hours(s)))


''' stats variables '''
stats_more_than_3_consecutive_working_days = 0
stats_more_than_3_consecutive_working_days_used = False
stats_more_than_4_days_per_week = 0
stats_more_than_4_days_per_week_used = False
stats_saturday_same_as_sunday = 0
stats_saturday_same_as_sunday_used = False
stats_not_enough_days_off_before_or_after_working_days = 0
stats_not_enough_days_off_before_or_after_working_days_used = False
stats_too_many_single_working_days = 0
stats_too_many_single_working_days_used = False
stats_more_than_48h_working_over_7_moving_days = 0
stats_more_than_48h_working_over_7_moving_days_used = False
stats_two_working_week_ends_in_a_row = 0
stats_two_working_week_ends_in_a_row_used = False
stats_not_enough_or_too_many_working_days_over_n_weeks = 0
stats_not_enough_or_too_many_working_days_over_n_weeks_used = False
stats_not_exactly_1_out_of_3_working_weekend = 0
stats_not_exactly_1_out_of_3_working_weekend_used = False
stats_monday_after_working_weekend = 0
stats_monday_after_working_weekend_used = False
stats_min_hours_per_month = 0
stats_max_hours_per_month = 0
stats_min_max_hours_per_month_used = False
stats_evening_then_morning = 0
stats_evening_then_morning_used = False


def reset_pruning_stats():
    global stats_more_than_3_consecutive_working_days
    global stats_more_than_3_consecutive_working_days_used
    global stats_more_than_4_days_per_week
    global stats_more_than_4_days_per_week_used
    global stats_saturday_same_as_sunday
    global stats_saturday_same_as_sunday_used
    global stats_not_enough_days_off_before_or_after_working_days
    global stats_not_enough_days_off_before_or_after_working_days_used
    global stats_too_many_single_working_days
    global stats_too_many_single_working_days_used
    global stats_more_than_48h_working_over_7_moving_days
    global stats_more_than_48h_working_over_7_moving_days_used
    global stats_two_working_week_ends_in_a_row
    global stats_two_working_week_ends_in_a_row_used
    global stats_not_enough_or_too_many_working_days_over_n_weeks
    global stats_not_enough_or_too_many_working_days_over_n_weeks_used
    global stats_not_exactly_1_out_of_3_working_weekend
    global stats_not_exactly_1_out_of_3_working_weekend_used
    global stats_monday_after_working_weekend
    global stats_monday_after_working_weekend_used
    global stats_min_hours_per_month
    global stats_max_hours_per_month
    global stats_min_max_hours_per_month_used
    global stats_evening_then_morning
    global stats_evening_then_morning_used
    print(" * reset pruning stats")
    stats_more_than_3_consecutive_working_days = 0
    stats_more_than_3_consecutive_working_days_used = False
    stats_more_than_4_days_per_week = 0
    stats_more_than_4_days_per_week_used = False
    stats_saturday_same_as_sunday = 0
    stats_saturday_same_as_sunday_used = False
    stats_not_enough_days_off_before_or_after_working_days = 0
    stats_not_enough_days_off_before_or_after_working_days_used = False
    stats_too_many_single_working_days = 0
    stats_too_many_single_working_days_used = False
    stats_more_than_48h_working_over_7_moving_days = 0
    stats_more_than_48h_working_over_7_moving_days_used = False
    stats_two_working_week_ends_in_a_row = 0
    stats_two_working_week_ends_in_a_row_used = False
    stats_not_enough_or_too_many_working_days_over_n_weeks = 0
    stats_not_enough_or_too_many_working_days_over_n_weeks_used = False
    stats_not_exactly_1_out_of_3_working_weekend = 0
    stats_not_exactly_1_out_of_3_working_weekend_used = False
    stats_monday_after_working_weekend = 0
    stats_monday_after_working_weekend_used = False
    stats_min_hours_per_month = 0
    stats_max_hours_per_month = 0
    stats_min_max_hours_per_month_used = False
    stats_evening_then_morning = 0
    stats_evening_then_morning_used = False


def print_pruning_stats():
    if stats_saturday_same_as_sunday_used:
        print(" * stats_saturday_same_as_sunday: {}".format(stats_saturday_same_as_sunday))
    if stats_more_than_3_consecutive_working_days_used:
        print(" * stats_more_than_3_consecutive_working_days: {}".format(stats_more_than_3_consecutive_working_days))
    if stats_more_than_4_days_per_week_used:
        print(" * stats_more_than_4_days_per_week: {}".format(stats_more_than_4_days_per_week))
    if stats_not_enough_days_off_before_or_after_working_days_used:
        print(" * stats_not_enough_days_off_before_or_after_working_days: {}".format(
            stats_not_enough_days_off_before_or_after_working_days))
    if stats_too_many_single_working_days_used:
        print(" * stats_too_many_single_working_days: {}".format(stats_too_many_single_working_days))
    if stats_more_than_48h_working_over_7_moving_days_used:
        print(" * stats_more_than_48h_working_over_7_moving_days: {}".format(
            stats_more_than_48h_working_over_7_moving_days))
    if stats_two_working_week_ends_in_a_row_used:
        print(" * stats_two_working_week_ends_in_a_row: {}".format(stats_two_working_week_ends_in_a_row))
    if stats_not_enough_or_too_many_working_days_over_n_weeks_used:
        print(" * stats_not_enough_or_too_many_working_days_over_n_weeks: {}".format(
            stats_not_enough_or_too_many_working_days_over_n_weeks))
    if stats_not_exactly_1_out_of_3_working_weekend_used:
        print(" * stats_not_exactly_1_out_of_3_working_weekend: {}".format(stats_not_exactly_1_out_of_3_working_weekend))
    if stats_monday_after_working_weekend_used:
        print(" * stats_monday_after_working_weekend: {}".format(stats_monday_after_working_weekend))
    if stats_min_max_hours_per_month_used:
        print(" * stats_min_hours_per_month: {}".format(stats_min_hours_per_month))
        print(" * stats_max_hours_per_month: {}".format(stats_max_hours_per_month))
    if stats_evening_then_morning_used:
        print(" * stats_evening_then_morning: {}".format(stats_evening_then_morning))


def assemble_variants_two_by_two(out_weeklen, in_file1, weeklen_file1, in_file2, weeklen_file2, out_file):
    print(" * assemble_variants_two_by_two")
    size_file_1 = stat(in_file1).st_size
    size_file_2 = stat(in_file2).st_size
    n_lines_file_1 = int(size_file_1 / (weeklen_file1 * 7 + 1))
    n_lines_file_2 = int(size_file_2 / (weeklen_file2 * 7 + 1))
    n_frames_to_keep = int(max_disk_usage_per_file / (out_weeklen * 7 + 1))
    to_be_generated = n_lines_file_1 * n_lines_file_2
    skip_cnt = round(to_be_generated / n_frames_to_keep)
    if to_be_generated > n_frames_to_keep:
        print(" * input_file 1 size {} bytes which represents {} variants".format(size_file_1, n_lines_file_1))
        print(" * input_file 2 size {} bytes which represents {} variants".format(size_file_2, n_lines_file_2))
        print(" * We must limit disk usage to {} bytes with frame generation of {} chars each".format(
            max_disk_usage_per_file, out_weeklen * 7 + 1))
        print(" * total number of possibilities {} x {} = {}".format(n_lines_file_1, n_lines_file_2, to_be_generated))
        print(" * Number of {}-weeks variants to keep to respect disk usage: {}".format(out_weeklen, n_frames_to_keep))

    cnt = 0
    sk_cnt = 0
    with open(out_file, 'w') as out:
        with open(in_file1) as f1:
            for l1 in f1:
                s1 = string_to_weekset(l1)
                with open(in_file2) as f2:
                    for l2 in f2:
                        if sk_cnt > skip_cnt:
                            sk_cnt = 0
                            s2 = string_to_weekset(l2)
                            ns = tuple(s1 + s2)
                            out.write(weekset_to_string(ns) + '\n')
                            cnt += 1
                        sk_cnt += 1
    print(" * total number of {}-weeks time possibilities before pruning {}".format(out_weeklen, cnt))


def set_has_saturday_same_as_sunday(s) -> bool:
    """ return true if saturday is not the same type as sunday """
    global stats_saturday_same_as_sunday
    global stats_saturday_same_as_sunday_used
    stats_saturday_same_as_sunday_used = True
    assert (len(s) == 7)
    if s[-1] != s[-2]:
        stats_saturday_same_as_sunday += 1
        return True
    return False


def set_has_more_than_48h_over_7_moving_days(s) -> bool:
    """ return true if a more than 48h of work over 7 rolling days """
    global stats_more_than_48h_working_over_7_moving_days
    global stats_more_than_48h_working_over_7_moving_days_used
    stats_more_than_48h_working_over_7_moving_days_used = True
    assert (len(s) % 7 == 0)
    for i in range(0, len(s) - 6):
        ss = tuple(s[i:7 + i])
        r = get_number_of_hours(ss)
        if r > 48:
            stats_more_than_48h_working_over_7_moving_days += 1
            return True
    return False


def set_has_two_working_week_ends_in_a_row(s) -> bool:
    global stats_two_working_week_ends_in_a_row
    global stats_two_working_week_ends_in_a_row_used
    stats_two_working_week_ends_in_a_row_used = True
    assert((len(s) % 7) == 0)
    assert(len(s) > 0)
    n_w = int(len(s)/7)
    if n_w == 1:
        return False
    prev = s[6]
    for i in range(1, n_w):
        nextwe = s[7*i+6]
        if is_a_working_day(prev) and is_a_working_day(nextwe):
            stats_two_working_week_ends_in_a_row += 1
            return True
        prev = nextwe
    return False


def set_has_monday_after_working_weekend(s) -> bool:
    global stats_monday_after_working_weekend
    global stats_monday_after_working_weekend_used
    stats_monday_after_working_weekend_used = True
    assert((len(s) % 7) == 0)
    assert(len(s) > 0)
    n_w = int(len(s)/7)
    for i in range(0, n_w):
        idx = 7*i+6
        if is_12h_working_day(s[idx]) and is_a_working_day(s[(idx+1)%len(s)]):
            stats_monday_after_working_weekend += 1
            return True
    return False


def set_out_of_min_max_working_hours_per_month(s):
    global stats_min_hours_per_month
    global stats_max_hours_per_month
    global stats_min_max_hours_per_month_used
    stats_min_max_hours_per_month_used = True
    assert(len(s) == 7*4)
    h = get_number_of_hours(s)
    if h < min_number_of_hours_per_month:
        stats_min_hours_per_month += 1
        return True
    if h > max_number_of_hours_per_month:
        stats_max_hours_per_month += 1
        return True
    return False


def set_has_not_1_out_3_working_weekend(s):
    global stats_not_exactly_1_out_of_3_working_weekend_used
    global stats_not_exactly_1_out_of_3_working_weekend
    stats_not_exactly_1_out_of_3_working_weekend_used = True
    assert(len(s) % 7 == 0)
    n_w = int(len(s)/7)
    assert(n_w >= 6)
    assert(n_w % 3 == 0)
    # printw_asptmc(s)
    # print_ephad_short(s)
    pattern = [is_a_working_day(s[6]), is_a_working_day(s[6+7]), is_a_working_day(s[6+14])]
    # print("pattern: {}".format(pattern))
    if pattern.count(True) != 1 or pattern.count(False) != 2:
        # print('KO1 {}'.format(s))
        stats_not_exactly_1_out_of_3_working_weekend += 1
        return True
    # print("pattern: {}".format(pattern))
    # print("num_week: {}".format(n_w))

    for i in range(3, n_w):
        # print("checking {} -> {}:{} --> {}:{}".format(i, 7*i+6, s[7*i+6], (i-3)%len(pattern), pattern[(i-3)%len(pattern)]))
        # print("is_a_working_day: {} pattern: {}".format(is_a_working_day(s[7*i+6]), pattern[(i-3)%len(pattern)]))
        if is_a_working_day(s[7*i+6]) != pattern[(i-3)%len(pattern)]:
            # print('KO2 {}'.format(s))
            stats_not_exactly_1_out_of_3_working_weekend += 1
            return True

    # print("OK {}".format(s))
    return False


def set_has_two_working_week_ends_in_a_row(s) -> bool:
    """ TO REWORK """
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


def set_has_too_many_single_working_days(s) -> bool:
    """ TO REWORK """
    global stats_too_many_single_working_days
    global stats_too_many_single_working_days_used
    stats_too_many_single_working_days_used = True
    a = ('J', 'o', 'J', 'o', 'J')
    if (any(a == s[i:len(a) + i] for i in range(len(s) - len(a) + 1))):
        stats_too_many_single_working_days += 1
        return True
    return False


def set_has_not_enough_days_off_before_or_after_working_days(s) -> bool:
    """ TO REWORK """
    ''' remove all variants which do not respect 2 days off after
        2 or 3 working days '''
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


def set_has_more_than_3_consecutive_working_days(s) -> bool:
    """ TO REWORK """
    global stats_more_than_3_consecutive_working_days
    global stats_more_than_3_consecutive_working_days_used
    stats_more_than_3_consecutive_working_days_used = True
    p = ('J', 'J', 'J', 'J')
    if any(p == s[i:len(p) + i] for i in range(len(s) - len(p) + 1)):
        stats_more_than_3_consecutive_working_days += 1
        return True
    return False


def set_has_more_than_4_days_per_week(s) -> bool:

    global stats_more_than_4_days_per_week
    global stats_more_than_4_days_per_week_used
    stats_more_than_4_days_per_week_used = True
    if s.count('J') > 4:
        stats_more_than_4_days_per_week += 1
        return True
    return False


def set_has_not_enough_or_too_many_working_days_over_n_weeks(s, mini, maxi) -> bool:
    """ TO REWORK """
    global stats_not_enough_or_too_many_working_days_over_n_weeks
    global stats_not_enough_or_too_many_working_days_over_n_weeks_used
    stats_not_enough_or_too_many_working_days_over_n_weeks_used = True
    c = s.count('J')
    if c < mini or c > maxi:
        stats_not_enough_or_too_many_working_days_over_n_weeks += 1
        return True
    return False