'''
Pour la génération du planning alternance jour / nuit, on va utiliser ce qui a été généré pour
la trame de jour et pour la trame de nuit.
On choisit arbitairement d'assembler 1 trames de 8 semaines de jour avec une trame de 8 semaines
de nuit. (on pourrait faire l'inverse mais ça ne change rien).

Pour la condition d'assemblage du jour avec la nuit, ça induit un changement de rythme et donc
attention.
La fin d'une trame de jour fini par un samedi / dimanche qui peuvent être:
- Soit repos
- Soit 12h
- Soit 7h30.

Le début d'une trame de nuit commence par un lundi / mardi qui peuvent être:
- Soit repos
- Soit 12h.

On autorise uniquement les assemblages suivants:
- Week end en jour de repos <--> n'importe quoi ensuite
- Week end en jour 12h <--> Repos Lundi Mardi
- Week end en jour 7h30 <--> Repos Lundi
'''

import sys
sys.path.append('../../00-common/src/')


from functions import string_to_weekset, weekset_to_string
from as_ptmc_functions import get_number_of_hours, is_a_working_day, is_12h_working_day, is_a_7h30_working_day, printw_asptmc
from itertools import permutations, product
from os.path import join, isfile
from os import makedirs, stat
import sys

results_dir = "../output"
variant_dir = join(results_dir, "variants_12w")


jour_w8_text_file = join(variant_dir, "jour-8-weeks.txt")
nuit_w8_text_file = join(variant_dir, "nuit-8-weeks.txt")
alt_w16_text_file = join(variant_dir, "alt-16-weeks.txt")
alt_w16_all_text_file = join(variant_dir, "alt-16-weeks-all-variants.txt")


''' 1Mo limit per file when stored '''
max_disk_usage_per_file = 1000000


stats_cannot_be_joint = 0
stats_cannot_be_joint_used = False


def reset_pruning_stats():
	global stats_cannot_be_joint
	global stats_cannot_be_joint_used
	print(" * reset pruning stats")
	stats_cannot_be_joint = 0
	stats_cannot_be_joint_used = False


def print_pruning_stats():
    if stats_cannot_be_joint_used:
        print(" * stats_cannot_be_joint: {}".format(stats_cannot_be_joint))


def assemble_variants_two_by_two(out_weeklen, in_file1, weeklen_file1, in_file2, weeklen_file2, out_file):
    print("assemble_variants_two_by_two")
    size_file_1 = stat(in_file1).st_size
    size_file_2 = stat(in_file2).st_size
    n_lines_file_1 = int(size_file_1 / (weeklen_file1*7+1))
    n_lines_file_2 = int(size_file_2 / (weeklen_file2*7+1))
    n_frames_to_keep = int(max_disk_usage_per_file / (out_weeklen*7+1))
    to_be_generated = n_lines_file_1 * n_lines_file_2
    skip_cnt = round(to_be_generated / n_frames_to_keep)
    if to_be_generated > n_frames_to_keep:
        print("input_file 1 size {} bytes which represents {} variants".format(size_file_1, n_lines_file_1))
        print("input_file 2 size {} bytes which represents {} variants".format(size_file_2, n_lines_file_2))
        print("We must limit disk usage to {} bytes with frame generation of {} chars each".format(max_disk_usage_per_file, out_weeklen*7+1))
        print("total number of possibilities {} x {} = {}".format(n_lines_file_1, n_lines_file_2, to_be_generated))
        print("Number of {}-weeks variants to keep to respect disk usage: {}".format(out_weeklen, n_frames_to_keep))

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
    print("total number of {}-weeks time possibilities before pruning {}".format(out_weeklen, cnt))


def sets_cannot_be_joined(s) -> bool:
    ''' remove from variants if 8w day variant cannot be joint with 8w night variant '''
    global stats_cannot_be_joint
    global stats_cannot_be_joint_used
    stats_cannot_be_joint_used = True
    assert(len(s) == 16*7)
    '''
    On autorise uniquement les assemblages suivants:
    - Week end en jour de repos <--> n'importe quoi ensuite
    - Week end en jour 12h <--> Repos Lundi Mardi
    - Week end en jour 7h30 <--> Repos Lundi
    '''
    idx = 7*8
    if  (is_12h_working_day(s[idx-1]) and (is_a_working_day(s[idx]) or is_a_working_day(s[idx+1]))) or \
        (is_a_7h30_working_day(s[idx-1]) and is_a_working_day(s[idx])):
        stats_cannot_be_joint += 1
        return True
    return False


def prune_weeks_variant(num_week, infile, outfile):
    assert(num_week in [16])
    print(' * Pruning {} weeks variant'.format(num_week))
    cnt = 0
    with open(outfile, 'w') as out:
        with open(infile) as f:
            for line in f:
                s = string_to_weekset(line)

                if num_week == 16:
                    if sets_cannot_be_joined(s):
                        continue

                out.write(weekset_to_string(s) + '\n')
                cnt += 1

    print_pruning_stats()
    reset_pruning_stats()
    print(' * [{}-week] After pruning, number of variants: {}'.format(num_week, cnt))


if __name__ == "__main__":

    ''' 16 weeks part '''
    if not isfile(alt_w16_all_text_file):
    	if not isfile(jour_w8_text_file):
    		raise ValueError("Error, file {} does not exists. It must be generated first".format(jour_w8_text_file))
    	if not isfile(nuit_w8_text_file):
    		raise ValueError("Error, file {} does not exists. It must be generated first".format(nuit_w8_text_file))
    	assemble_variants_two_by_two(16, jour_w8_text_file, 8, nuit_w8_text_file, 8, alt_w16_all_text_file)

    if not isfile(alt_w16_text_file):
        prune_weeks_variant(16, alt_w16_all_text_file, alt_w16_text_file)
    else:
        print("file {} already exists, using it".format(alt_w16_text_file))
