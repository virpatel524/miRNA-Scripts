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



	pd_disjac = pd.DataFrame.sort(pd.DataFrame(tmp_disjac, columns=['Jaccard Similarity Coefficient', 'Age (MY)', 'miRNA Class', 'Type']),columns=['Type', 'Age (MY)'])
	pd_expjac = pd.DataFrame.sort(pd.DataFrame(tmp_expjac, columns=['Jaccard Similarity Coefficient', 'Age (MY)', 'miRNA Class', 'Type']),columns=['Type', 'Age (MY)'])
	pd_tarjac = pd.DataFrame.sort(pd.DataFrame(tmp_tarjac, columns=['Jaccard Similarity Coefficient', 'Age (MY)', 'miRNA Class', 'Type']),columns=['Type', 'Age (MY)'])
	
	f, (ax1, ax2, ax3) = sns.plt.subplots(3, 1, sharex=True, sharey=True)



	sns.boxplot(x='Age (MY)', y='Jaccard Similarity Coefficient', hue='miRNA Class', data=pd_expjac, showfliers=False, ax=ax1)
	sns.boxplot(x='Age (MY)', y='Jaccard Similarity Coefficient', hue='miRNA Class', data=pd_tarjac, showfliers=False, ax=ax2)
	sns.boxplot(x='Age (MY)', y='Jaccard Similarity Coefficient', hue='miRNA Class', data=pd_disjac, showfliers=False, ax=ax3)

	ax1.set_ylabel('')
	ax3.set_ylabel('')
	ax3.legend_.remove()
	ax2.legend_.remove()


	ax1.set_xlabel('')
	ax2.set_xlabel('')

	ax1.legend(loc='upper right', frameon=True).get_frame().set_edgecolor('b')

	f.subplots_adjust(hspace=0.3)
	sns.plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

	sns.plt.savefig('../figures/disjac_fig.pdf',bbox_inches='tight')
	sns.plt.close()





def genfig2():
	f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = sns.plt.subplots(2, 3)

	pd_binary_disnum = pd.DataFrame.sort(pd.DataFrame(mirbinary_disnum, columns=['Number of Diseases', 'Age (MY)', 'miRNA Class', 'Type']),columns=['miRNA Class', 'Age (MY)'],ascending=[False, True])
	pd_binary_expnum = pd.DataFrame.sort(pd.DataFrame(mirbinary_expnum, columns=['Number of Tissues', 'Age (MY)', 'miRNA Class', 'Type']),columns=['miRNA Class', 'Age (MY)'],ascending=[False, True])
	pd_binary_tarnum = pd.DataFrame.sort(pd.DataFrame(mirbinary_tarnum, columns=['Number of Targets', 'Age (MY)', 'miRNA Class', 'Type']),columns=['miRNA Class', 'Age (MY)'],ascending=[False, True])
	pd_strat_disnum = pd.DataFrame.sort(pd.DataFrame(mirstrat_disnum, columns=['Number of Diseases', 'Age (MY)', 'miRNA Class', 'Type']),columns=['miRNA Class', 'Age (MY)'],ascending=[False, True])
	pd_strat_expnum = pd.DataFrame.sort(pd.DataFrame(mirstrat_expnum, columns=['Number of Tissues', 'Age (MY)', 'miRNA Class', 'Type']),columns=['miRNA Class', 'Age (MY)'],ascending=[False, True])
	pd_strat_tarnum = pd.DataFrame.sort(pd.DataFrame(mirstrat_tarnum, columns=['Number of Targets', 'Age (MY)', 'miRNA Class', 'Type']),columns=['miRNA Class', 'Age (MY)'],ascending=[False, True])

	sns.boxplot(x='miRNA Class', y='Number of Tissues', data=pd_binary_expnum, showfliers=False, ax=ax1)
	sns.boxplot(x='miRNA Class', y='Number of Targets',  data=pd_binary_tarnum, showfliers=False, ax=ax2)
	sns.boxplot(x='miRNA Class', y='Number of Diseases',  data=pd_binary_disnum, showfliers=False, ax=ax3)
	sns.boxplot(x='Age (MY)', y='Number of Tissues', hue='miRNA Class', data=pd_strat_expnum, showfliers=False, ax=ax4)
	sns.boxplot(x='Age (MY)', y='Number of Targets', hue='miRNA Class', data=pd_strat_tarnum, showfliers=False, ax=ax5)
	sns.boxplot(x='Age (MY)', y='Number of Diseases', hue='miRNA Class', data=pd_strat_disnum, showfliers=False, ax=ax6)

	ax5.legend(loc='upper left', frameon=True).get_frame().set_edgecolor('b')
	ax4.legend_.remove()
	ax6.legend_.remove()
	f.subplots_adjust(hspace=0.3)
	sns.plt.show()

	sns.plt.savefig('../figures/num_allthreefig.pdf')





# mirbinary_disjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disjac')))
# mirbinary_expjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_expjac')))
# mirbinary_tarjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarjac')))
mirbinary_disnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disnum')))
mirbinary_expnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tisnum')))
mirbinary_tarnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarnum')))

# mirstrat_disjac = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_disjac')))
# mirstrat_expjac = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tisjac')))
# mirstrat_tarjac = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarjac')))
mirstrat_disnum = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_disnum')))
mirstrat_expnum = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_expnum')))
mirstrat_tarnum = append_haveage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirstrat_tarnum')))






genfig2()