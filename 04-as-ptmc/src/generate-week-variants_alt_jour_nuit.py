'''
Pour la génération du planning alternance jour / nuit, on va utiliser ce qui a été généré pour
la trame de jour et pour la trame de nuit.

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

from as_ptmc_functions import *
from os.path import join, isfile

jour_w9_text_file = join(variant_dir, "jour-9-weeks.txt")
nuit_w9_text_file = join(variant_dir, "nuit-9-weeks.txt")
alt_w18_text_file = join(variant_dir, "alt-18-weeks.txt")
alt_w18_all_text_file = join(variant_dir, "alt-18-weeks-all-variants.txt")

stats_cannot_be_joint = 0
stats_cannot_be_joint_used = False


def sets_cannot_be_joined(s) -> bool:
    ''' remove from variants if 8w day variant cannot be joint with 8w night variant '''
    global stats_cannot_be_joint
    global stats_cannot_be_joint_used
    stats_cannot_be_joint_used = True
    assert (len(s) == 18 * 7)
    '''
    On autorise uniquement les assemblages suivants:
    - Week end en jour de repos <--> n'importe quoi ensuite
    - Week end en jour 12h <--> Repos Lundi Mardi
    - Week end en jour 7h30 <--> Repos Lundi
    '''
    idx = 7 * 8
    if (is_12h_working_day(s[idx - 1]) and (is_a_working_day(s[idx]) or is_a_working_day(s[idx + 1]))) or \
            (is_a_7h30_working_day(s[idx - 1]) and is_a_working_day(s[idx])):
        stats_cannot_be_joint += 1
        return True
    return False


def prune_weeks_variant(num_week, infile, outfile):
    assert (num_week == 18)
    print(' * Pruning {} weeks variant'.format(num_week))
    cnt = 0
    with open(outfile, 'w') as out:
        with open(infile) as f:
            for line in f:
                s = string_to_weekset(line)

                if sets_cannot_be_joined(s):
                    continue

                if set_has_not_1_out_3_working_weekend(s):
                    continue

                out.write(weekset_to_string(s) + '\n')
                cnt += 1

    print_pruning_stats()
    reset_pruning_stats()
    print(' * [{}-week] After pruning, number of variants: {}'.format(num_week, cnt))


if __name__ == "__main__":

    ''' 18 weeks part '''
    if not isfile(alt_w18_all_text_file):
        if not isfile(jour_w9_text_file):
            raise ValueError("Error, file {} does not exists. It must be generated first".format(jour_w9_text_file))
        if not isfile(nuit_w9_text_file):
            raise ValueError("Error, file {} does not exists. It must be generated first".format(nuit_w9_text_file))
        assemble_variants_two_by_two(18, jour_w9_text_file, 9, nuit_w9_text_file, 9, alt_w18_all_text_file)

    if not isfile(alt_w18_text_file):
        prune_weeks_variant(18, alt_w18_all_text_file, alt_w18_text_file)
    else:
        print("file {} already exists, using it".format(alt_w18_text_file))
