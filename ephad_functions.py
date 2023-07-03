def is_working_day(l):
    return l in ['m','s','a','b','c']


def is_a_rest_day(l):
    return l == 'z'


def is_12h_working_day(l):
    return l in ['a','b','c']


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


def printw_ephad(s):
    d = {
        'm': ' matin',
        's': '  soir',
        'a': '   12h',
        'z': '   repos'
    }
    assert(len(s)%7 == 0)
    nb_w = int(len(s)/7)
    jours_semaine = 'Lundi Mardi Mercredi Jeudi Vendredi Samedi Dimanche'
    jours_semaine_formate = ' '.join([j.ljust(11) for j in jours_semaine.split()])
    print(jours_semaine_formate)
    for i in range(0, nb_w):
        for j in range(0, 7):
            print("{}".format(d[s[j+7*i]]).ljust(12), end='')
        print()
    print(" -- days:{}/{}".format(7*nb_w - s.count('z'), len(s)), end='')
    print(" hours: {}h".format(get_number_of_hours(s)))


def print_ephad_short(s):
    assert(len(s)%7 == 0)
    nb_w = int(len(s)/7)
    print()
    ''' to enable line print header, override nb_w to 1 '''
    for i in range(0, 1):
        print("L M M J V S D ", end='')
    print()
    for i in range(0, nb_w):
        for j in range(0, 7):
            print("{} ".format(s[j+7*i]), end='')
        print()
    print("days worked: {}/{}".format(7*nb_w - s.count('z'), len(s)))
