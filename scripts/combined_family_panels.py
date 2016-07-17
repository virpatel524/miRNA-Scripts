from general_methods import * 
import seaborn as sns
import pandas as pd

def allages_cmp(el1, el2):
	if type(el1) == str:
		return -1
	if type(el2) == str:
		return 1
	if el2 == el1:
		return 0
	if el1 > el2:
		return 1
	if el2 > el1:
		return -1



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
		alpha.append(1)
	return tmp

def append_haveage(lst):
	tmp = lst[:]
	for alpha in tmp:
		alpha.append(0)

	return tmp

def genfig1():
	tmp_disjac = sorted(mirbinary_disjac + mirstrat_disjac, cmp=allages_cmp)
	tmp_expjac = sorted(mirbinary_expjac + mirstrat_expjac, cmp=allages_cmp)
	tmp_tarjac = sorted(mirbinary_tarjac + mirstrat_tarjac, cmp=allages_cmp)
	tmp_disnum = sorted(mirbinary_disnum + mirstrat_disnum, cmp=allages_cmp)
	tmp_expnum = sorted(mirbinary_expnum + mirstrat_expnum, cmp=allages_cmp)
	tmp_tarnum = sorted(mirbinary_tarnum + mirstrat_tarnum, cmp=allages_cmp)


	pd_disjac = pd.DataFrame.sort(pd.DataFrame(tmp_disjac, columns=['Jaccard', 'Age (MY)', 'miRNA Class', 'Type']),columns=['Type', 'Age (MY)'])
	pd_expjac = pd.DataFrame.sort(pd.DataFrame(tmp_expjac, columns=['Jaccard', 'Age (MY)', 'miRNA Class', 'Type']),columns=['Type', 'Age (MY)'])
	pd_pd.DataFrame.sort(pd.DataFrame(tmp_tarjac, columns=['Jaccard', 'Age (MY)', 'miRNA Class', 'Type']),columns=['Type', 'Age (MY)'])


	sns.boxplot(x='Age (MY)', y='Jaccard', hue='miRNA Class', data=tmp,  showfliers=False)
	sns.plt.show()
	sns.plt.close()





mirbinary_disjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disjac')))
mirbinary_expjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_expjac')))
mirbinary_tarjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarjac')))
mirbinary_disnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disnum')))
mirbinary_expnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tisnum')))
mirbinary_tarnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarnum')))

mirstrat_disjac = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_disjac')))
mirstrat_expjac = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tisjac')))
mirstrat_tarjac = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarjac')))
mirstrat_disnum = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_disnum')))
mirstrat_expnum = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_expnum')))
mirstrat_tarnum = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarnum')))


genfig1()