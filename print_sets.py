def printw(s):
    assert(len(s)%7 == 0)
    nb_w = int(len(s)/7)
    print()
    # to enable line print header, override nb_w to 1
    # for i in range(0, nb_w):
    for i in range(0, 1):
        print("L M M J V S D ", end='')
    print()
    for i in range(0, nb_w):
        for j in range(0, 7):
        #for e in s:
            print("{} ".format(s[j+7*i]), end='')
        print()
    print("days worked: {}".format(s.count('J')))


def load_wset_from_file(filename):
    print("Loading wset from {}".format(filename))
    r = []
    with open(filename) as file:
        for line in file:
            #  print(line)
            r.append(tuple(line.rstrip()))
    return set(r)


if __name__ == "__main__":
    input_file = "output/variants_12w/12-weeks.txt"

    ampwv = load_wset_from_file(input_file)

    for s in ampwv:
        printw(s)

