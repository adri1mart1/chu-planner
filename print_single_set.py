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


def string_to_weekset(s):
    return tuple(s.rstrip())


if __name__ == "__main__":
    s_string = input("which set: ")
    print(s_string)

    printw(string_to_weekset(s_string))
