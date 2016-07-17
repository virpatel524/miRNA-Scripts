from general_methods import * 


def num(s):
	try:
		return float(s)
	except:
		return s

def float_conv(entry):
	 return [[num(a) for a in beta] for beta in entry]








mirbinary_disjac = (parsecsvexport('../relevant_data/precursor_pd/mirbinary_disjac'))
mirbinary_expjac = parsecsvexport('../relevant_data/precursor_pd/mirbinary_expjac')
mirbinary_tarjac = parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarjac')
mirbinary_disnum = parsecsvexport('../relevant_data/precursor_pd/mirbinary_disnum')
mirbinary_expnum = parsecsvexport('../relevant_data/precursor_pd/mirbinary_tisnum')
mirbinary_tarnum = parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarnum')

mirstrat_disjac = parsecsvexport('../relevant_data/precursor_pd/mirstrat_disjac')
mirstrat_expjac = parsecsvexport('../relevant_data/precursor_pd/mirstrat_tisjac')
mirstrat_tarjac = parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarjac')
mirstrat_disnum = parsecsvexport('../relevant_data/precursor_pd/mirstrat_disnum')
mirstrat_expnum = parsecsvexport('../relevant_data/precursor_pd/mirstrat_expnum')
mirstrat_tarnum = parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarnum')




