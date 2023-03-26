'''
Ce fichier va tenter de permettre l'élaboration d'un planning pour un ephad.

Actuellement, le service est entièrement en 7h30. Il y a donc 3 personnes
le matin, 2 l'après midi pour une charge totale sur la journée de:
  (3+2)x7,5 = 37,5h.
L'objectif est de garder environ cette charge mais d'avoir au mieux 4 personnes
par weekend.
Théoriquement, en montant jusqu'à 12h par jour, on peut s'approcher du volume de
travail avec 3 personnes (3x12h = 36h).

Condition:
 - Equipe de 10 personnes (pas de temps partiel considéré)
 - au moins 1 personne entre 6h30 et à 21h
 - 48h max de travail sur 7 jours glissants
 - En semaine en, le travail est et reste en 7h30.
   Les horaires: 6h30 / 14h30 ... 13h30 / 21H
 - Une journée typique: 3 personnes le matin, 2p l'apres midi
 - Temps partiels dans l'équipe:
     1 personne à 80%
     1 personne à 90%
     2 personnes à 50%
   (Ne pas considérer les temps partiels dans un 1er temps)
 - Le trame ne doit pas faire plus de 12 semaines
 - Un travail le samedi implique le dimanche
 - Si une journée de plus de 7h30 de travail le weekend, récup le lundi
 - Essayer de ne pas changer d'horaire sur le weekend
 - La durée min d'une journée de travail est de 7h30
   La durée max d'une journée de travail est de 12h
 - Le matin un peu plus tendu pour la toilette (comprendre
   qu'il faut privilégier plus de monde le matin, au moins 2 personnes
   à partir de 8h)

Output:
 - Soit fournir une trame avec les JCA (marge)
 - Soit 3x12h le WE mais travail 1 WE/3

Souhaits de l'équipe:
 - L'équipe prefère bosser 1 weekend sur 3 quitte à faire + d'heure par jour
   Travailler un week end sur 2 est OK. Un entre 2 est envisageable.

Stratégie d'implémentation possibles:
 - version 1:
   construire la meme logique que pour la réa, construire les trames de semaines
   possibles et les combiner 2 à 2 en prunant au fur et à mesure.

   A: réfléchir uniquement en 12h sur le weekend
   B: réfléchir a des variantes d'horaires

 - version 2:
   utiliser un pool de personnes disponibles avec priorisation sur les gens qui
   n'ont pas travaillé depuis longtemps

---
Version 1-A:

Définition d'une trame sur une semaine:
Du lundi au vendredi:
 - m: matin (matin)
 - s: soir
 - z: off
Samedi et Dimanche:
 - a: 12h-6h30
 - b: 12h-8h
 - c: 12h-9h
 - z: off
'''

from functions import string_to_weekset, weekset_to_string
from itertools import permutations, product
from os.path import join, isfile
from os import makedirs, stat
import sys

# store all 1week variant raw
all_1w_raw = []

# store all 1week variant pruned
all_1w_pruned = []


results_dir = "output_ephad"
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


''' 10Mb limit per file when stored '''
max_disk_usage_per_file = 10000000


''' stats variables '''
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


def print_pruning_stats():
    global stats_more_than_3_consecutive_working_days
    global stats_more_than_4_days_per_week
    global stats_saturday_nor_sunday
    global stats_not_enough_days_off_before_or_after_working_days
    global stats_too_many_single_working_days
    global stats_more_than_48h_working_over_7_moving_days
    global stats_two_working_week_ends_in_a_row
    global stats_not_enough_or_too_many_working_days_over_n_weeks
    global stats_not_exactly_1_out_of_3_working_weekend
    global stats_more_than_one_3_working_days_in_a_row
    if stats_more_than_3_consecutive_working_days_used:
        print(" * stats_more_than_3_consecutive_working_days: {}".format(stats_more_than_3_consecutive_working_days))
    if stats_more_than_4_days_per_week_used:
        print(" * stats_more_than_4_days_per_week: {}".format(stats_more_than_4_days_per_week))
    if stats_saturday_nor_sunday_used:
        print(" * stats_saturday_nor_sunday: {}".format(stats_saturday_nor_sunday))
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


def printw(s):
    d = {
        'm': '   matin',
        's': '    soir',
        'a': '12h-6h30',
        'b': '  12h-8h',
        'c': '  12h-9h',
        'z': '   repos'
    }
    assert(len(s)%7 == 0)
    nb_w = int(len(s)/7)
    print()
    jours_semaine = 'Lundi Mardi Mercredi Jeudi Vendredi Samedi Dimanche'
    jours_semaine_formate = ' '.join([j.ljust(11) for j in jours_semaine.split()])
    print(jours_semaine_formate)
    for i in range(0, nb_w):
        for j in range(0, 7):
            print("{}".format(d[s[j+7*i]]).ljust(12), end='')
        print()
    print(" -- days:{}/{}".format(7*nb_w - s.count('z'), len(s)), end='')
    print(" hours: {}h".format(get_number_of_hours(s)))


def is_working_day(l):
    return l in ['m','s','a','b','c']


def generate_1week_variant():
    global all_1w_raw
    all_mon_to_fri_raw = set(permutations("".join("m"*5 + "s"*5 + "z"*5), 5))
    # we consider at the moment we do the same shift between saturday and sunday
    all_sat_to_sun_raw = {('a','a'), ('b','b'), ('c','c'), ('z','z')}
    all_week = list(set(product(all_mon_to_fri_raw, all_sat_to_sun_raw)))
    for w in all_week:
        all_1w_raw.append(tuple(sum(w, ())))
    all_1w_raw = set(all_1w_raw)
    with open(w1_all_text_file, 'w') as out:
        for w in all_1w_raw:
            out.write(weekset_to_string(w) + '\n')
    print(' * [1week] Number of possible permutations: {}'.format(len(all_1w_raw)))


def get_number_of_hours(s) -> float:
    d = {
        'a': 12,
        'b': 12,
        'c': 12,
        'm': 7.5,
        's': 7.5,
        'z': 0
    }
    return sum(d[val] for val in s)

def set_has_more_than_48h_over_7_moving_days(s) -> bool:
    global stats_more_than_48h_working_over_7_moving_days
    global stats_more_than_48h_working_over_7_moving_days_used
    stats_more_than_48h_working_over_7_moving_days_used = True
    ''' return true if a more than 48h of work over 7 rolling days '''
    assert(len(s)%7 == 0)
    for i in range(0, len(s)-7):
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
    prev = ""
    for i in range(0, n_w):
        if prev == s[7*i+6] and is_working_day(prev):
            stats_two_working_week_ends_in_a_row += 1
            return True
        prev = s[7*i+6]
    return False


def prune_1week_variant():
    print(' * Pruning 1w variant')
    cnt = 0
    with open(w1_text_file, 'w') as out:
        with open(w1_all_text_file) as f:
            for line in f:
                s = string_to_weekset(line)

                if set_has_more_than_48h_over_7_moving_days(s):
                    continue
                if set_has_saturday_nor_sunday(s):
                    continue

                out.write(weekset_to_string(s) + '\n')
                cnt += 1

    print_pruning_stats()
    reset_pruning_stats()
    print(' * [1week] After pruning, number of variants: {}'.format(cnt))


def prune_2weeks_variant():
    print(' * Pruning 2w variant')
    cnt = 0
    with open(w2_text_file, 'w') as out:
        with open(w2_all_text_file) as f:
            for line in f:
                s = string_to_weekset(line)

                if set_has_more_than_48h_over_7_moving_days(s):
                    continue

                if set_has_two_working_week_ends_in_a_row(s):
                    continue

                out.write(weekset_to_string(s) + '\n')
                cnt += 1

    print_pruning_stats()
    reset_pruning_stats()
    print(' * [1week] After pruning, number of variants: {}'.format(cnt))



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

    ''' 1 week part '''
    if not isfile(w1_text_file):
        generate_1week_variant()
        prune_1week_variant()
    else:
        print(" * file {} already exists, using it".format(w1_text_file))

    ''' 2 weeks part '''
    if not isfile(w2_all_text_file):
        assemble_variants_two_by_two(2, w1_text_file, 1, w1_text_file, 1, w2_all_text_file)
    if not isfile(w2_text_file):
        prune_2weeks_variant()
    else:
        print(" * file {} already exists, using it".format(w2_text_file))

    # for w in all_1w_pruned:
        # printw(w)