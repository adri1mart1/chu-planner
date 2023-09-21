"""
Hypotheses:
 - Chaque jour, on peut soit:
   - être de repos (o)
   - soit être au travail en 12h (J)
   - soit être au travail en 7h30 (M)
"""

from as_ptmc_functions import *
from itertools import permutations
from os.path import join, isfile


w1_all_text_file = join(variant_dir, "jour-1-week-all.txt")
w1_text_file = join(variant_dir, "jour-1-week.txt")
w2_text_file = join(variant_dir, "jour-2-weeks.txt")
w2_all_text_file = join(variant_dir, "jour-2-weeks-all-variants.txt")
w3_text_file = join(variant_dir, "jour-3-weeks.txt")
w3_all_text_file = join(variant_dir, "jour-3-weeks-all-variants.txt")
w6_text_file = join(variant_dir, "jour-6-weeks.txt")
w6_all_text_file = join(variant_dir, "jour-6-weeks-all-variants.txt")
w9_text_file = join(variant_dir, "jour-9-weeks.txt")
w9_all_text_file = join(variant_dir, "jour-9-weeks-all-variants.txt")
w18_text_file = join(variant_dir, "jour-18-weeks.txt")
w18_all_text_file = join(variant_dir, "jour-18-weeks-all-variants.txt")


def generate_1week_variant():
    global all_1w_raw
    all_1w_raw = set(permutations("".join("o" * 7 + "J" * 7 + "M" * 7), 7))
    assert (len(all_1w_raw) == 3 ** 7)
    with open(w1_all_text_file, 'w') as out:
        for w in all_1w_raw:
            out.write(weekset_to_string(w) + '\n')
    print(' * [1week] Number of possible permutations: {}'.format(len(all_1w_raw)))


def prune_weeks_variant(num_week, infile, outfile):
    assert (num_week in [1, 2, 3, 6, 9, 18])
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

                if num_week in [6, 9, 18]:
                    if set_has_not_1_out_3_working_weekend(s):
                        continue

                out.write(weekset_to_string(s) + '\n')
                cnt += 1

    print_pruning_stats()
    reset_pruning_stats()
    print(' * [{}-week] After pruning, number of variants: {}'.format(num_week, cnt))


if __name__ == "__main__":
    print(' * Starting')

    ''' 1 week raw '''
    if not isfile(w1_all_text_file):
        generate_1week_variant()
    else:
        print(" * file {} already exists, using it".format(w1_all_text_file))

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

    ''' 3 weeks part '''
    if not isfile(w3_all_text_file):
        assemble_variants_two_by_two(3, w2_text_file, 2, w1_text_file, 1, w3_all_text_file)
    if not isfile(w3_text_file):
        prune_weeks_variant(3, w3_all_text_file, w3_text_file)
    else:
        print(" * file {} already exists, using it".format(w3_text_file))

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
        prune_weeks_variant(9, w9_all_text_file, w9_text_file)
    else:
        print(" * file {} already exists, using it".format(w9_text_file))

    ''' 18 weeks parts '''
    if not isfile(w18_all_text_file):
        assemble_variants_two_by_two(18, w9_text_file, 9, w9_text_file, 9, w18_all_text_file)
    if not isfile(w18_text_file):
        prune_weeks_variant(18, w18_all_text_file, w18_text_file)
    else:
        print(" * file {} already exists, using it".format(w18_text_file))
