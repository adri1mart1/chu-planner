import itertools

a = ('o','J','a', 'b','c')
w = set(itertools.product(a, repeat=5))
print(w)
print(len(w))
x = set(itertools.permutations(a, 2))
print(x)
print("length:{}".format(len(x)))
y = set(itertools.permutations(x, 2))
print(y)
print("length:{}".format(len(y)))
z = set(itertools.permutations(a, 4))
print(z)
print("length:{}".format(len(z)))
