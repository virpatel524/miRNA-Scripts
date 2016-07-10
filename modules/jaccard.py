def jaccard_calculate(a,b):
	p = 0
	q = 0
	r = 0
	s = 0
	if sum(a) == 0 and sum(b) == 0: return 1.0

	for i in range(len(a)):
		if a[i] == 1 and b[i] == 1:
			p += 1
		if a[i] == 1 and b[i] == 0:
			q += 1
		if a[i] == 0 and b[i] == 1:
			r += 1
		if a[i] == 0 and b[i] == 0:
			s += 1

	return 1.0 - float(q + r) / float(p + q + r)