s = "JooJoJJooJoJooJJooJoooJJJoooJJoooJJooJJoooJoJooJJoooJJooJJooJoooJJooJJoooJJooJoJJoooJJoooJJooJoJoooJoJoooJoJooJJoooJJooJJooJoooJJJoooJoJooJJ"
a = s.replace('o', '-')

n_w = int(len(a)/7)
for i in range(n_w):
	for j in range(7):
		print("{}".format(a[7*i+j]), end='')
	print()