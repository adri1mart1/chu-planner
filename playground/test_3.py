x = ('J', 'J', 'J', 'J', 'o', 'o', 'J')
p = ('J', 'J', 'J', 'J')
print(any(p == x[i:len(p) + i] for i in range(len(x) - len(p) + 1)))

q = ('J', 'o', 'J')
print(any(q == x[i:len(q) + i] for i in range(len(x) - len(q) + 1)))
