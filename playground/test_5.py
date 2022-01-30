sh = "oJJooJJooJJoooJooJJooJJooJooJoJooJJooJJooooJooJJJoooJJooJJooJooJoJooJJooJJooooJoJJooJoJooJJooJJoooJJoooJJoooJJoooJoJJooJoJooJJooJJoooJJooJoo"
s1 = "oJJooJJooJJoooJooJJooJJooJooJoJooJJooJJooooJooJJJoooJJooJJooJooJoJooJJooJJooooJoJJooJoJooJJooJJoooJJoooJJoooJJoooJoJJooJoJooJJooJJoooJJooJoo"
s2 = "ooJJoooJooJJooJJooJooJoJooJJooJJooooJooJJJoooJJooJJooJooJoJooJJooJJooooJoJJooJoJooJJooJJoooJJoooJJoooJJoooJoJJooJoJooJJooJJoooJJooJoooJJooJJ"
s3 = "JooJJooJJooJooJoJooJJooJJooooJooJJJoooJJooJJooJooJoJooJJooJJooooJoJJooJoJooJJooJJoooJJoooJJoooJJoooJoJJooJoJooJJooJJoooJJooJoooJJooJJooJJooo"
s4 = "JJooJooJoJooJJooJJooooJooJJJoooJJooJJooJooJoJooJJooJJooooJoJJooJoJooJJooJJoooJJoooJJoooJJoooJoJJooJoJooJJooJJoooJJooJoooJJooJJooJJoooJooJJoo"
s5 = "JoJooJJooJJooooJooJJJoooJJooJJooJooJoJooJJooJJooooJoJJooJoJooJJooJJoooJJoooJJoooJJoooJoJJooJoJooJJooJJoooJJooJoooJJooJJooJJoooJooJJooJJooJoo"

b = sh.replace("o", "-")
print("shift:")
n_w = int(len(sh)/7)
for i in range(n_w):
	for j in range(7):
		print("{}".format(b[7*i+j]), end='')
	print()
print("{}".format(s1.replace("o", "-")))
print("{}".format(s2.replace("o", "-")))
print("{}".format(s3.replace("o", "-")))
print("{}".format(s4.replace("o", "-")))
print("{}".format(s5.replace("o", "-")))
