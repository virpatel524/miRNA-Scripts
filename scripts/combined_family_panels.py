from general_methods import * 


def num(s):
	try:
		return float(s)
	except:
		return s

def float_conv(entry):
	 return [[num(a) for a in beta] for beta in entry]


def append_allage(lst):
	newlst = []
	for alpha in lst:
		newlst.append(lst.insert(1, 'ALL AGES'))
	return newlst






mirbinary_disjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disjac'))
mirbinary_expjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_expjac'))
mirbinary_tarjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarjac'))
mirbinary_disnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disnum'))
mirbinary_expnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tisnum'))
mirbinary_tarnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarnum'))

mirstrat_disjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_disjac'))
mirstrat_expjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tisjac'))
mirstrat_tarjac = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarjac'))
mirstrat_disnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_disnum'))
mirstrat_expnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_expnum'))
mirstrat_tarnum = float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarnum'))



