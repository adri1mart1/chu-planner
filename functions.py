def printw(s):
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
    print("days worked: {}".format(s.count('J')))


def string_to_weekset(s):
    return tuple(s.rstrip())


def weekset_to_string(s):
    return ''.join(s)


def load_wset_from_file(filename):
    print("Loading wset from {}".format(filename))
    r = []
    with open(filename) as file:
        for line in file:
            r.append(tuple(line.split(' ')[-1].rstrip()))
    return set(r)


def count_subtuple_in_tuple(b, a):
    r = 0
    for i in range(len(b)-len(a)+1):
        r += 1 if a == b[i:len(a) + i] else 0
    return r


def save_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content)
