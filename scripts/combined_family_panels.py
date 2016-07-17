from general_methods import * 
import seaborn as sns
import pandas as pd


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
	tmp_disjac = mirbinary_disjac + mirstrat_disjac
	tmp_expjac = mirbinary_expjac + mirstrat_expjac
	tmp_tarjac = mirbinary_tarjac + mirstrat_tarjac
	tmp_disnum = mirbinary_disnum + mirstrat_disnum
	tmp_expnum = mirbinary_expnum + mirstrat_expnum
	tmp_tarnum = mirbinary_tarnum + mirstrat_tarnum

	tmp = pd.DataFrame(tmp_disjac, columns=['Jaccard', 'Age (MY)', 'miRNA Class'])

	sns.boxplot(x='Age (MY)', y='Jaccard', hue='miRNA Class', data=tmp)
	sns.plt.show()
	sns.plt.close()







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

genfig1()

