'''
Hypotheses:
 - Chaque jour, on peut soit:
   - être de repos (o)
   - soit être au travail en 12h (D)
   - soit être au travail en 7h30 (C)

'''

import sys
sys.path.append('../../00-common/src/')


from functions import string_to_weekset, weekset_to_string
from urg_ped_functions import get_number_of_hours, is_a_working_day
from itertools import permutations, product
from os.path import join, isfile
from os import makedirs, stat
import sys

# store all 1week variant raw
all_1w_raw = []

# store all 1week variant pruned
all_1w_pruned = []


results_dir = "../output"
variant_dir = join(results_dir, "variants_12w")
w1_all_text_file = join(variant_dir, "1-week-all.txt")
w1_text_file = join(variant_dir, "1-week.txt")
w2_text_file = join(variant_dir, "2-weeks.txt")
w2_all_text_file = join(variant_dir, "2-weeks-all-variants.txt")
w4_text_file = join(variant_dir, "4-weeks.txt")
w4_all_text_file = join(variant_dir, "4-weeks-all-variants.txt")
w8_text_file = join(variant_dir, "8-weeks.txt")
w8_all_text_file = join(variant_dir, "8-weeks-all-variants.txt")
w12_text_file = join(variant_dir, "12-weeks.txt")
w12_all_text_file = join(variant_dir, "12-weeks-all-variants.txt")


''' 1Mo limit per file when stored '''
max_disk_usage_per_file = 1000000


''' global min/max variables
actual working time is 37,5h per week. That means 5 days of 7,5h of work.
Over 4 weeks, it's 150h (4x37,5). '''

min_number_of_hours_per_month = 126
max_number_of_hours_per_month = 174


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
stats_more_than_one_3_working_days_in_a_row = 0
stats_more_than_one_3_working_days_in_a_row_used = False
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
    global stats_more_than_one_3_working_days_in_a_row
    global stats_more_than_one_3_working_days_in_a_row_used
    global stats_monday_after_working_weekend
    global stats_monday_after_working_weekend_used
    print(" * reset pruning stats")
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
    stats_more_than_48h_working_over_7_moving_days = 0
    stats_more_than_48h_working_over_7_moving_days_used = False
    stats_two_working_week_ends_in_a_row = 0
    stats_two_working_week_ends_in_a_row_used = False
    stats_not_enough_or_too_many_working_days_over_n_weeks = 0
    stats_not_enough_or_too_many_working_days_over_n_weeks_used = False
    stats_not_exactly_1_out_of_3_working_weekend = 0
    stats_not_exactly_1_out_of_3_working_weekend_used = False
    stats_more_than_one_3_working_days_in_a_row = 0
    stats_more_than_one_3_working_days_in_a_row_used = False
    stats_monday_after_working_weekend = 0
    stats_monday_after_working_weekend_used = False
    stats_min_hours_per_month = 0
    stats_max_hours_per_month = 0
    stats_min_max_hours_per_month_used = False
    stats_evening_then_morning = 0
    stats_evening_then_morning_used = False


def print_pruning_stats():
    global stats_more_than_3_consecutive_working_days
    global stats_more_than_4_days_per_week
    global stats_saturday_same_as_sunday
    global stats_not_enough_days_off_before_or_after_working_days
    global stats_too_many_single_working_days
    global stats_more_than_48h_working_over_7_moving_days
    global stats_two_working_week_ends_in_a_row
    global stats_not_enough_or_too_many_working_days_over_n_weeks
    global stats_not_exactly_1_out_of_3_working_weekend
    global stats_more_than_one_3_working_days_in_a_row
    global stats_monday_after_working_weekend
    if stats_saturday_same_as_sunday_used:
        print(" * stats_saturday_same_as_sunday: {}".format(stats_saturday_same_as_sunday))
    if stats_more_than_3_consecutive_working_days_used:
        print(" * stats_more_than_3_consecutive_working_days: {}".format(stats_more_than_3_consecutive_working_days))
    if stats_more_than_4_days_per_week_used:
        print(" * stats_more_than_4_days_per_week: {}".format(stats_more_than_4_days_per_week))
    if stats_not_enough_days_off_before_or_after_working_days_used:
        print(" * stats_not_enough_days_off_before_or_after_working_days: {}".format(stats_not_enough_days_off_before_or_after_working_days))
    if stats_too_many_single_working_days_used:
        print(" * stats_too_many_single_working_days: {}".format(stats_too_many_single_working_days))
    if stats_more_than_48h_working_over_7_moving_days_used:
        print(" * stats_more_than_48h_working_over_7_moving_days: {}".format(stats_more_than_48h_working_over_7_moving_days))
    if stats_two_working_week_ends_in_a_row_used:
        print(" * stats_two_working_week_ends_in_a_row: {}".format(stats_two_working_week_ends_in_a_row))
    if stats_not_enough_or_too_many_working_days_over_n_weeks_used:
        print(" * stats_not_enough_or_too_many_working_days_over_n_weeks: {}".format(stats_not_enough_or_too_many_working_days_over_n_weeks))
    if stats_not_exactly_1_out_of_3_working_weekend_used:
        print(" * stats_not_exactly_1_out_of_3_working_weekend: {}".format(stats_not_exactly_1_out_of_3_working_weekend))
    if stats_more_than_one_3_working_days_in_a_row_used:
        print(" * stats_more_than_one_3_working_days_in_a_row: {}".format(stats_more_than_one_3_working_days_in_a_row))
    if stats_monday_after_working_weekend_used:
        print(" * stats_monday_after_working_weekend: {}".format(stats_monday_after_working_weekend))
    if stats_min_max_hours_per_month_used:
        print(" * stats_min_hours_per_month: {}".format(stats_min_hours_per_month))
        print(" * stats_max_hours_per_month: {}".format(stats_max_hours_per_month))
    if stats_evening_then_morning_used:
        print(" * stats_evening_then_morning: {}".format(stats_evening_then_morning))


def generate_1week_variant():
    global all_1w_raw
    all_1w_raw = set(permutations("".join("o"*7 + "D"*7 + "C"*7), 7))
    assert(len(all_1w_raw) == 3**7)
    with open(w1_all_text_file, 'w') as out:
        for w in all_1w_raw:
            out.write(weekset_to_string(w) + '\n')
    print(' * [1week] Number of possible permutations: {}'.format(len(all_1w_raw)))


def set_has_saturday_same_as_sunday(s) -> bool:
    ''' remove from variants if saturday is not the same type as sunday '''
    global stats_saturday_same_as_sunday
    global stats_saturday_same_as_sunday_used
    stats_saturday_same_as_sunday_used = True
    assert(len(s) == 7)
    if s[-1] != s[-2]:
        stats_saturday_same_as_sunday += 1
        return True
    return False


def set_has_evening_then_morning(s) -> bool:
    global stats_evening_then_morning
    global stats_evening_then_morning_used
    stats_evening_then_morning_used = True
    assert(len(s)%7 == 0)
    for i in range(0, len(s)-1):
        if s[i] == 's' and s[i+1] == 'm':
            return True
    return False


def set_has_more_than_48h_over_7_moving_days(s) -> bool:
    global stats_more_than_48h_working_over_7_moving_days
    global stats_more_than_48h_working_over_7_moving_days_used
    stats_more_than_48h_working_over_7_moving_days_used = True
    ''' return true if a more than 48h of work over 7 rolling days '''
    assert(len(s)%7 == 0)
    for i in range(0, len(s)-6):
        ss = tuple(s[i:7+i])
        r = get_number_of_hours(ss)
        if r > 48:
            stats_more_than_48h_working_over_7_moving_days += 1
            return True
    return False


def set_has_saturday_nor_sunday(s) -> bool:
    ''' return true if saturday is a working day and sunday is not and vice versa '''
    assert(len(s) == 7)
    not_working = 'z'

    if  s[-1] == not_working and s[-2] != not_working or \
        s[-1] != not_working and s[-2] == not_working:
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
        if is_12h_working_day(s[idx]) and is_working_day(s[(idx+1)%len(s)]):
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
    assert(len(s)%7 == 0)
    n_w = int(len(s)/7)
    assert(n_w >= 4)
    # print_ephad_short(s)
    pattern = [s[6], s[6+7], s[6+14]]
    if pattern.count('z') != 2 or pattern.count('a') != 1:
        # print('KO, first 3 weeks doesnt respect pattern {}'.format(pattern))
        return True
    # print("pattern: {}".format(pattern))
    # print("num_week: {}".format(n_w))

    for i in range(2, n_w):
        # print("checking {}".format(i))
        if s[7*i+6] != pattern[i%len(pattern)]:
            # print('KO, doesnt respect pattern {}'.format(pattern))
            return True

    # print("OK")
    return False


def prune_weeks_variant(num_week, infile, outfile):
    assert(num_week in [1,2,4,8,12])
    print(' * Pruning {} weeks variant'.format(num_week))
    cnt = 0
    with open(outfile, 'w') as out:
        with open(infile) as f:
            for line in f:
                s = string_to_weekset(line)

                if num_week == 1:
                    if set_has_saturday_same_as_sunday(s):
                        continue

                if set_has_more_than_48h_over_7_moving_days(s):
                    continue

                if set_has_two_working_week_ends_in_a_row(s):
                    continue

                # if set_has_monday_after_working_weekend(s):
                #     continue

                if num_week >= 4:
                    if set_has_not_1_out_3_working_weekend(s):
                        continue

                if num_week == 4:
                    if set_out_of_min_max_working_hours_per_month(s):
                        continue

                out.write(weekset_to_string(s) + '\n')
                cnt += 1

    print_pruning_stats()
    reset_pruning_stats()
    print(' * [{}-week] After pruning, number of variants: {}'.format(num_week, cnt))



def assemble_variants_two_by_two(out_weeklen, in_file1, weeklen_file1, in_file2, weeklen_file2, out_file):
    print(" * assemble_variants_two_by_two")
    size_file_1 = stat(in_file1).st_size
    size_file_2 = stat(in_file2).st_size
    n_lines_file_1 = int(size_file_1 / (weeklen_file1*7+1))
    n_lines_file_2 = int(size_file_2 / (weeklen_file2*7+1))
    n_frames_to_keep = int(max_disk_usage_per_file / (out_weeklen*7+1))
    to_be_generated = n_lines_file_1 * n_lines_file_2
    skip_cnt = round(to_be_generated / n_frames_to_keep)
    if to_be_generated > n_frames_to_keep:
        print(" * input_file 1 size {} bytes which represents {} variants".format(size_file_1, n_lines_file_1))
        print(" * input_file 2 size {} bytes which represents {} variants".format(size_file_2, n_lines_file_2))
        print(" * We must limit disk usage to {} bytes with frame generation of {} chars each".format(max_disk_usage_per_file, out_weeklen*7+1))
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
                        sk_cnt +=1
    print(" * total number of {}-weeks time possibilities before pruning {}".format(out_weeklen, cnt))


if __name__ == "__main__":
    print(' * Starting')

    makedirs(results_dir, exist_ok=True)
    makedirs(variant_dir, exist_ok=True)

    ''' 1 week raw '''
    if not isfile(w1_all_text_file):
        generate_1week_variant()

    ''' 1 week part '''
    if not isfile(w1_text_file):
        prune_weeks_variant(1, w1_all_text_file, w1_text_file)
    else:
        print(" * file {} already exists, using it".format(w1_text_file))

    ''' 2 weeks part '''
    if not isfile(w2_all_text_file):
        assemble_variants_two_by_two(2, w1_text_file, 1, w1_text_file, 1, w2_all_text_file)
    if not isfile(w2_text_file):
        prune_weeks_variant(2, w2_all_text_file, w2_text_file)
    else:
        print(" * file {} already exists, using it".format(w2_text_file))

    ''' 4 weeks part '''
    if not isfile(w4_all_text_file):
        assemble_variants_two_by_two(4, w2_text_file, 2, w2_text_file, 2, w4_all_text_file)
    if not isfile(w4_text_file):
        prune_weeks_variant(4, w4_all_text_file, w4_text_file)
    else:
        print(" * file {} already exists, using it".format(w4_text_file))

    sys.exit(0)

    ''' 8 weeks part '''
    if not isfile(w8_all_text_file):
        assemble_variants_two_by_two(8, w4_text_file, 4, w4_text_file, 4, w8_all_text_file)
    if not isfile(w8_text_file):
        prune_weeks_variant(8, w8_all_text_file, w8_text_file)
    else:
        print(" * file {} already exists, using it".format(w8_text_file))

    ''' 12 weeks parts '''
    if not isfile(w12_all_text_file):
        assemble_variants_two_by_two(12, w8_text_file, 8, w4_text_file, 4, w12_all_text_file)
    if not isfile(w12_text_file):
        prune_weeks_variant(12, w12_all_text_file, w12_text_file)
    else:
        print(" * file {} already exists, using it".format(w12_text_file))