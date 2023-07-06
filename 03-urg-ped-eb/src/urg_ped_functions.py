
def get_number_of_hours(s) -> float:
    d = {
        'o': 0,
        'D': 12,
        'C': 7.5
    }
    return sum(d[val] for val in s)


def is_a_working_day(l):
    return l in ['D','C']


def printw_urgped(s):
    d = {
        'o': 'off',
        'D': '12h',
        'C': '7.5'
    }
    assert(len(s)%7 == 0)
    nb_w = int(len(s)/7)
    jours_semaine = 'Lun Mar Mer Jeu Ven Sam Dim'
    jours_semaine_formate = ' '.join([j.ljust(4) for j in jours_semaine.split()])
    print(jours_semaine_formate)
    for i in range(0, nb_w):
        for j in range(0, 7):
            print("{}".format(d[s[j+7*i]]).ljust(5), end='')
        print()
    # print(" -- days:{}/{}".format(7*nb_w - s.count('z'), len(s)), end='')
    # print(" hours: {}h".format(get_number_of_hours(s)))
