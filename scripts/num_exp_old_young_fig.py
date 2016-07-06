import seaborn as sns
import pandas as pd
import csv


def age_parser(age_txt):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(age_txt,delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])

	with open('../relevant_data/hsa_all_mir_lst.txt','w') as mirlst:
		for mirna in mirna2age:
			mirlst.write(mirna + '\n')
			


	return mirna2age, age2mirna


def sortmir(mirna2age, mir_expdb):
	newlst = []

	for val in mir_expdb.index:
		alpha =  sum(mir_expdb.loc[val].tolist())
		if val in mirna2age:
			if float(mirna2age[val]) < 100.0:
				newlst.append([alpha, 'Under 100.0 MY'])
			else:
				newlst.append([alpha, 'Over 100.0 MY'])

	return pd.DataFrame(newlst, columns=['Number of Tissues Expressed In', 'miRNA Age'])


def genfig(db):
	sns.violinplot(x='miRNA Age', y='Number of Tissues Expressed In',data=db, cut=0)
	sns.plt.gca().set_ylim([0,20])
	sns.plt.savefig('../figures/mir_old_yung_tisexp_violinplot.pdf',bbox_inches='tight')

	sns.plt.close()

	sns.boxplot(x='miRNA Age', y='Number of Tissues Expressed In',data=db)
	sns.plt.gca().set_ylim([0,20])
	sns.plt.savefig('../figures/mir_old_yung_tisexp_boxplot.pdf',bbox_inches='tight')

	sns.plt.close()


mir_expdb = pd.read_csv('../relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
agedb = '../relevant_data/allmir_ages/hsa_family_file_ph_allmir_dollo_age-time.protein_list'
mirna2age, age2mirna = age_parser(open(agedb, 'r'))

fig_db = sortmir(mirna2age, mir_expdb)

genfig(fig_db)





