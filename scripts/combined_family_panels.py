from general_methods import * 


def num(s):
	try:
		return float(s)
	except:
		return s

def float_conv(entry):
	 return [[num(a) for a in beta] for beta in entry]


def append_allage(lst):
	tmp = lst[:]
	for alpha in tmp:
		alpha.insert(1, 'ALL AGES')

	return tmp

def genfig1():
	









mirbinary_disjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disjac')))
mirbinary_expjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_expjac')))
mirbinary_tarjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarjac')))
mirbinary_disnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disnum')))
mirbinary_expnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tisnum')))
mirbinary_tarnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarnum')))

mirstrat_disjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_disjac'))
mirstrat_expjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tisjac'))
mirstrat_tarjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarjac'))
mirstrat_disnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_disnum'))
mirstrat_expnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_expnum'))
mirstrat_tarnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarnum'))



