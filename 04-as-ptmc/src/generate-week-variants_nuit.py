from as_ptmc_functions import *
from itertools import permutations, product
from os import makedirs
from os.path import join, isfile

'''
each month, we may work between 11 and 13 days which is
11 x 12 = 132 hours and 13 x 12 = 156 hours
A standard contract is 37.5 hours per week. With 12 hours working days
shift, that 3 days of 12 hours, 36 hours of work per week.
1,5 hour is missing so 12 hours / 1,5 hours = 8.
Every 8 weeks, an extra days of work must be worked to have a perfect
balance with 37,5 hours of work per week.
Ex: 8 weeks schedule: 7 weeks of 3 working days + 1 week of 4 working days
7 x 3 + 4 = 25 workings days, 25 x 12 hours = 300 hours.
300 hours / 37,5 = 8 weeks.

When combining 4-weeks units together, we need to aim for 25 days of work
exactly, hence, only one possibility exists which is combining a month of
12 days of work with a month of 13 days of work (and vice versa)
Considering 11 + 14 makes a too huge difference.
'''
min_nb_working_days_per_week = 2
max_nb_working_days_per_week = 4
min_nb_working_days_per_month = 11
max_nb_working_days_per_month = 14
min_nb_working_days_per_2months = 24
max_nb_working_days_per_2months = 26


w1_text_file = join(variant_dir, "nuit-1-week.txt")
w1_all_text_file = join(variant_dir, "nuit-1-week-all-variants.txt")
w2_text_file = join(variant_dir, "nuit-2-weeks.txt")
w2_all_text_file = join(variant_dir, "nuit-2-weeks-all-variants.txt")
w3_text_file = join(variant_dir, "nuit-3-weeks.txt")
w3_all_text_file = join(variant_dir, "nuit-3-weeks-all-variants.txt")
w6_text_file = join(variant_dir, "nuit-6-weeks.txt")
w6_all_text_file = join(variant_dir, "nuit-6-weeks-all-variants.txt")
w9_text_file = join(variant_dir, "nuit-9-weeks.txt")
w9_all_text_file = join(variant_dir, "nuit-9-weeks-all-variants.txt")
w18_text_file = join(variant_dir, "nuit-18-weeks.txt")
w18_all_text_file = join(variant_dir, "nuit-18-weeks-all-variants.txt")


def generate_1week_variant():
    global all_1w_raw
    all_1w_raw = set(permutations("".join("o" * 7 + "J" * 7), 7))
    assert(len(all_1w_raw) == 128)
    with open(w1_all_text_file, 'w') as out:
        for s in all_1w_raw:
            out.write(weekset_to_string(s) + '\n')
    print(' * [1week] Number of possible permutations: {}'.format(len(all_1w_raw)))


def prune_weeks_variant(num_week, infile, outfile):
    assert (num_week in [1, 2, 3, 6, 12, 15, 18])
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

                if num_week == 4:
                    if set_out_of_min_max_working_hours_per_month(s):
                        continue

                if num_week in [6, 9, 12, 15, 18]:
                    if set_has_not_1_out_3_working_weekend(s):
                        continue

                """
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


                # 2w

                if set_has_more_than_4_working_days_over_7_moving_days(s):
                    continue

                if set_has_two_working_week_ends_in_a_row(s):
                    continue

                if set_has_not_enough_or_too_many_working_days_over_n_weeks(s, min_nb_working_days_per_week*2, max_nb_working_days_per_week*2):
                    continue


                # 4w
                if set_has_not_exactly_1_out_of_3_working_weekend(s):
                    continue

                if set_has_more_than_one_3_working_days_in_a_row(s):
                    continue

                if set_has_not_enough_or_too_many_working_days_over_n_weeks(s, min_nb_working_days_per_month, max_nb_working_days_per_month):
                    continue

                if set_has_not_enough_days_off_before_or_after_working_days(s):
                    continue

                if set_has_more_than_4_working_days_over_7_moving_days(s):
                    continue

                if set_has_two_working_week_ends_in_a_row(s):
                    continue

                if set_has_too_many_single_working_days(s):
                    continue


                ''' check thread rotation by creating subset 
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
                '''
                """

                out.write(weekset_to_string(s) + '\n')
                cnt += 1

    print_pruning_stats()
    reset_pruning_stats()
    print(' * [{}-week] After pruning, number of variants: {}'.format(num_week, cnt))


if __name__ == "__main__":

    makedirs(results_dir, exist_ok=True)
    makedirs(variant_dir, exist_ok=True)

    ''' 1 week part '''
    if not isfile(w1_text_file):
        generate_1week_variant()
        prune_weeks_variant(1, w1_all_text_file, w1_text_file)
    else:
        print("file {} already exists, using it".format(w1_text_file))

    ''' 2 weeks part '''
    if not isfile(w2_all_text_file):
        assemble_variants_two_by_two(2, w1_text_file, 1, w1_text_file, 1, w2_all_text_file)
    if not isfile(w2_text_file):
        prune_weeks_variant(2, w2_all_text_file, w2_text_file)
    else:
        print("file {} already exists, using it".format(w2_text_file))

    ''' 3 weeks part '''
    if not isfile(w3_all_text_file):
        assemble_variants_two_by_two(3, w2_text_file, 2, w1_text_file, 1, w3_all_text_file)
    if not isfile(w3_text_file):
        prune_weeks_variant(3, w3_all_text_file, w3_text_file)
    else:
        print("file {} already exists, using it".format(w3_text_file))

    ''' 6 weeks part '''
    if not isfile(w6_all_text_file):
        assemble_variants_two_by_two(6, w3_text_file, 3, w3_text_file, 3, w6_all_text_file)
    if not isfile(w6_text_file):
        prune_weeks_variant(6, w6_all_text_file, w6_text_file)
    else:
        print(" * file {} already exists, using it".format(w6_text_file))

    ''' 9 weeks parts '''
    if not isfile(w9_all_text_file):
        assemble_variants_two_by_two(9, w6_text_file, 6, w3_text_file, 3, w9_all_text_file)
    if not isfile(w9_text_file):
        prune_weeks_variant(12, w9_all_text_file, w9_text_file)
    else:
        print(" * file {} already exists, using it".format(w9_text_file))

    ''' 18 weeks parts '''
    if not isfile(w18_all_text_file):
        assemble_variants_two_by_two(18, w9_text_file, 9, w9_text_file, 9, w18_all_text_file)
    if not isfile(w18_text_file):
        prune_weeks_variant(18, w18_all_text_file, w18_text_file)
    else:
        print(" * file {} already exists, using it".format(w18_text_file))
