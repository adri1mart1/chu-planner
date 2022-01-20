import itertools

a = {
     ('o', 'o', 'J', 'o', 'J', 'o', 'o'),
     ('J', 'J', 'J', 'o', 'o', 'o', 'o'),
     ('o', 'J', 'J', 'o', 'o', 'o', 'o'),
     ('J', 'o', 'o', 'J', 'o', 'J', 'J'),
     ('o', 'o', 'o', 'o', 'o', 'J', 'J'),
     ('o', 'o', 'J', 'o', 'o', 'J', 'J'),
     ('o', 'J', 'o', 'o', 'J', 'J', 'J'),
     ('o', 'J', 'o', 'o', 'o', 'J', 'J'),
     ('o', 'o', 'o', 'J', 'o', 'J', 'J'),
     ('J', 'J', 'o', 'o', 'J', 'o', 'o'),
     ('o', 'o', 'J', 'o', 'o', 'o', 'o'),
     ('o', 'o', 'o', 'J', 'J', 'o', 'o'),
     ('o', 'o', 'J', 'J', 'o', 'o', 'o'),
     ('J', 'o', 'o', 'o', 'J', 'o', 'o'),
     ('J', 'o', 'J', 'o', 'o', 'o', 'o'),
     ('o', 'J', 'o', 'o', 'o', 'o', 'o'),
     ('o', 'o', 'o', 'o', 'o', 'o', 'o'),
     ('o', 'J', 'o', 'o', 'J', 'o', 'o'),
     ('o', 'o', 'o', 'J', 'o', 'o', 'o'),
     ('o', 'o', 'J', 'J', 'J', 'o', 'o'),
     ('o', 'J', 'o', 'J', 'o', 'o', 'o'),
     ('J', 'o', 'o', 'J', 'o', 'o', 'o'),
     ('o', 'J', 'J', 'J', 'o', 'o', 'o'),
     ('J', 'o', 'o', 'o', 'o', 'J', 'J'),
     ('J', 'o', 'o', 'J', 'J', 'o', 'o'),
     ('o', 'o', 'o', 'o', 'J', 'J', 'J'),
     ('o', 'J', 'J', 'o', 'o', 'J', 'J'),
     ('J', 'o', 'J', 'J', 'o', 'o', 'o'),
     ('o', 'J', 'o', 'J', 'J', 'o', 'o'),
     ('J', 'o', 'o', 'o', 'o', 'o', 'o'),
     ('J', 'o', 'o', 'o', 'J', 'J', 'J'),
     ('J', 'o', 'J', 'o', 'o', 'J', 'J'),
     ('J', 'J', 'o', 'o', 'o', 'o', 'o'),
     ('o', 'o', 'o', 'o', 'J', 'o', 'o'),
     ('J', 'J', 'o', 'o', 'o', 'J', 'J')
}

'''
Base: 35 éléments
Nombre de permutations: à 2 examplaires:      1 190 -> 0s
Nombre de permutations: à 3 examplaires:     39 270 -> 0s
Nombre de permutations: à 4 examplaires:  1 256 640 -> 2s
Nombre de permutations: à 5 examplaires: 38 955 840 -> 56s
Nombre d'éléments = n! / (n-r)!
avec n, le nombre d'éléments de base
    r, la longueur des combinaisons
'''
print("length a:{}".format(len(a)))
w = set(itertools.permutations(a, 2))
print("length w:{}".format(len(w)))
x = set(itertools.permutations(a, 3))
print("length x:{}".format(len(x)))
y = set(itertools.permutations(a, 4))
print("length y:{}".format(len(y)))
z = set(itertools.permutations(a, 5))
print("length z:{}".format(len(z)))
