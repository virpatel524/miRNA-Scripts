import seaborn
import pandas

def sort_mir(txt,txt2):
	mega_mir_lst = []
	famdict = {}
	mirlst_by_species = {}
	human_mirlst = {}

	meglst = [alpha[0] for alpha in list(csv.reader(txt,delimiter='\t'))]
	famlst = [alpha for alpha in list(csv.reader(txt2,delimiter='\t'))]

	for mir in meglst:
		species = mir[0:3]
		if species in bad_lst:
			continue
		if species[-1] == 'v':
			continue
		mega_mir_lst.append(mir)


		mirlst_by_species.setdefault(species,[]).append(mir)
	
	current_fam = ''

	for i in famlst:
		lst = [alpha for alpha in i[0].split(' ') if alpha != '']
		if i[0][:2] == 'ID' : 
			current_fam = lst[1]
		if i[0][:2] == 'MI' :
			if lst[2][:3] in bad_lst: continue
			if 'v' in lst[2].split('-')[0]: continue
			if lst[2] not in mega_mir_lst: continue
			else:
				famdict.setdefault(current_fam,[]).append(lst[2])

	for key in famdict:
		new_lst  = [a for a in famdict[key] if 'hsa' in a]
		if len(new_lst) > 1:
			human_mirlst[key] = new_lst


	family_file_for_mirbase = open('../relevant_data/family_file_ph_selectmir.txt','w')

	for i in famdict:
		for mir in famdict[i]:
			if mir != famdict[i][-1]:
				family_file_for_mirbase.write('%s|mirBase:%s ' %(mir[:3], mir)) 
			else: family_file_for_mirbase.write('%s|mirBase:%s\n' %(mir[:3], mir)) 

	family_file_for_mirbase.close()

	return mega_mir_lst, mirlst_by_species, human_mirlst 

def age_parser(age_txt):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(age_txt,delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])

	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/hsa_all_mir_lst.txt','w') as mirlst:
		for mirna in mirna2age:
			mirlst.write(mirna + '\n')
			


	return mirna2age, age2mirna







def parse_target_data(tardb,taragedb,timetreedb):

	mirna2target = {}
	tar2age = {}
	clade2age = {}

	parsed_tar = []
	parsed_ages = []

	master_tarlst = []




	with open(tardb) as tardb_fle:
		parsed_tar = [a for a in list(csv.reader(tardb_fle,delimiter='\t') ) if len(a) > 1]
		for alpha in parsed_tar:
			mirna2target.setdefault(alpha[0],[]).append(alpha[1])
		

	master_tarlst = list(set([item for sublist in mirna2target.values() for item in sublist]))

	clades = [a for a in list(csv.reader(open(timetreedb),delimiter='\t') ) if '#' not in a[0]]

	gene2age = {}
	clade2age = {}

	for alpha in clades:
		clade2age[alpha[0]] = float(alpha[1])


	gene_ages_raw = [a for a in list(csv.reader(open(taragedb),delimiter='\t') ) if '#' not in a[0]]




	return mirna2target, tar2age





def map_relatives(dic):
	newdic = {}

	for key in dic:
		for el in dic[key]:
			newdic[el] = [a for a in dic[key] if a != el]

	return newdic



def violin_nocomp(lst_for_exclusion, binary_data_frame, tipo,xentry,df_name):
	yes = []
	datalst = []
	no = []

	for alpha in binary_data_frame.index:
		if alpha in lst_for_exclusion:
			datalst.append([sum(binary_data_frame.loc[alpha].tolist()),'%s miRNAs' %(tipo)])
			yes.append(sum(binary_data_frame.loc[alpha].tolist()))
		else:
			datalst.append([sum(binary_data_frame.loc[alpha].tolist()),'Non-%s miRNAs' %(tipo)])
			no.append(sum(binary_data_frame.loc[alpha].tolist()))


	print mean(yes), mean(no)
	print median(yes), median(no)
	print mannwhitneyu(yes, no)


	data_master = pd.DataFrame(datalst,columns=[xentry, 'miRNA Class'])
	sns.violinplot(x='miRNA Class',y=xentry,data=data_master, cut=0)
	if 'tis' in df_name:
		plt.gca().set_ylim([0,20])
	if 'tar' in df_name:
		plt.gca().set_ylim([0,1000])
	plt.savefig('figures/nocomp_violin_%s.pdf' %(df_name),bbox_inches='tight')
	plt.close()



def violin_comp_norel(lst_for_exclusion, hamming_df, tipo,xentry,df_name):
	yes = []
	no = []

	datalst = []


	for alpha in hamming_df.index:
		for beta in hamming_df.index:
			if alpha == beta: continue
			if alpha in lst_for_exclusion and beta in lst_for_exclusion:
				datalst.append([float(hamming_df[alpha][beta]), '%s miRNAs' %(tipo)])
				yes.append(float(hamming_df[alpha][beta]))
			else:
				datalst.append([float(hamming_df[alpha][beta]), 'Non-%s miRNAs' %(tipo)])
				no.append(float(hamming_df[alpha][beta]))


	print mean(yes), mean(no)
	print median(yes), median(no)
	print mannwhitneyu(yes, no)


	data_master = pd.DataFrame(datalst,columns=[xentry, 'miRNA Class'])

	if 'tis' in df_name:
		sns.boxplot(x='miRNA Class',y=xentry,data=data_master)
		plt.gca().set_ylim([0,1.0])
		plt.savefig('figures/comp_norel_boxplot_%s.pdf' %(df_name),bbox_inches='tight')
		plt.close()

	if 'tar' in df_name:
		sns.violinplot(x='miRNA Class',y=xentry,data=data_master, cut=0)
		plt.gca().set_ylim([0,0.10])
		plt.savefig('figures/comp_norel_violin_%s.pdf' %(df_name),bbox_inches='tight')
		plt.close()



def violin_comp_rel(gen_exlus_dic, hamming_df, tipo, xentry, df_name):
	yes = []
	no = []

	datalst = []


	flipped_exlus = map_relatives(gen_exlus_dic)


	for alpha in hamming_df.index:
		for beta in hamming_df.index:
			if alpha == beta: continue
			if alpha in flipped_exlus:
				if beta in flipped_exlus[alpha]: 
					datalst.append([float(hamming_df[alpha][beta]), '%s miRNAs' %(tipo)])
					yes.append(float(hamming_df[alpha][beta]))
				else:
					datalst.append([float(hamming_df[alpha][beta]), 'Non-%s miRNAs' %(tipo)])
					no.append(float(hamming_df[alpha][beta]))
			else:
				datalst.append([float(hamming_df[alpha][beta]), 'Non-%s miRNAs' %(tipo)])
				no.append(float(hamming_df[alpha][beta]))




	print mean(yes), mean(no)
	print median(yes), median(no)
	print mannwhitneyu(yes, no)

	data_master = pd.DataFrame(datalst,columns=[xentry, 'miRNA Class'])

	if 'tis' in df_name:
		sns.boxplot(x='miRNA Class',y=xentry,data=data_master)
		plt.gca().set_ylim([0.0,1.0])
		plt.savefig('figures/comp_rel_boxplot_%s.pdf' %(df_name),bbox_inches='tight')
		plt.close()

	if 'tar' in df_name:
		sns.violinplot(x='miRNA Class',y=xentry,data=data_master, cut=0)
		plt.gca().set_ylim([0.0,0.10])
		plt.savefig('figures/comp_rel_violin_%s.pdf' %(df_name),bbox_inches='tight')
		plt.close()



def violin_comp_rel_ratio(gen_exlus_dic, hamming_df, tipo, xentry, df_name, new_df):
	yes = []
	no = []

	datalst = []


	flipped_exlus = map_relatives(gen_exlus_dic)

	genmirtar = [str(a) for a in list(new_df.index)]




	for alpha in hamming_df.index:
		print alpha
		for beta in hamming_df.index:
			if alpha == beta: continue
			if alpha in genmirtar and beta in genmirtar:
				if alpha in flipped_exlus:
					if beta in flipped_exlus[alpha]: 
						datalst.append([float(hamming_df[alpha][beta]), '%s miRNAs' %(tipo)])
						yes.append(	float(hamming_df[alpha][beta]) / (float(100) / float(sum(new_df.loc[alpha]))))
					else:
						datalst.append([float(hamming_df[alpha][beta]), 'Non-%s miRNAs' %(tipo)])
						no.append(	float(hamming_df[alpha][beta]) / (float(100) / float(sum(new_df.loc[alpha]))))
				else:
					datalst.append([float(hamming_df[alpha][beta]), 'Non-%s miRNAs' %(tipo)])
					no.append(float(hamming_df[alpha][beta]) / (float(100) / float(sum(new_df.loc[alpha]))))







	print mean(yes), mean(no)
	print median(yes), median(no)
	print mannwhitneyu(yes, no)

	data_master = pd.DataFrame(datalst,columns=[xentry, 'miRNA Class'])

	if 'tis' in df_name:
		sns.boxplot(x='miRNA Class',y=xentry,data=data_master)
		plt.savefig('figures/comp_rel_boxplot_%s.pdf' %(df_name),bbox_inches='tight')
		plt.close()

	if 'tar' in df_name:
		sns.violinplot(x='miRNA Class',y=xentry,data=data_master, cut=0)
		plt.savefig('figures/comp_rel_violinratio_%s.pdf' %(df_name),bbox_inches='tight')
		plt.close()






def heatmap_analysis(mirna2age, mirna2disease, mirna2family, gene2age):

	round_robyn_target = pd.read_csv('../relevant_data/target_heatmap_dataframe.txt', sep='\t',index_col=[0])
	round_robyn_exp = pd.read_csv('../relevant_data/tis_exp_heatmap_dataframe.txt', sep='\t',index_col=[0])
	mir_expdb = pd.read_csv('../relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
	mir_targetdb = pd.read_csv('../relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')

	mirna2family_edited = {}

	for alpha in mirna2family:
		if len(mirna2family[alpha]) > 3:
			mirna2family_edited[alpha] = mirna2family[alpha]

	mir_in_fam = flatten(mirna2family_edited.values())
	mir_notin_fam = []

	for mir in mirna2age:
		if mir not in flatten(mirna2family.values()):
			mir_notin_fam.append(mir)


	count1 = 0
	count2 = 0

	mir_num_dis_fam = []
	mir_num_dis_nofam = []

	for mirna in mir_in_fam:
		if mirna in mirna2disease:
			mir_num_dis_fam.append(len(mirna2disease[mirna]))
			count1 += 1


	for mirna in mir_notin_fam:
		if mirna in mirna2disease:
			mir_num_dis_nofam.append(len(mirna2disease[mirna]))
			count2 += 1

	# print float(count1) / float(len(mir_in_fam))
	# print float(count2) / float(len(mir_notin_fam))


	# print mean(mir_num_dis_fam), median(mir_num_dis_fam)

	# print mean(mir_num_dis_nofam), median(mir_num_dis_nofam)


	# print 'Number, Disease, Targets'

	# violin_nocomp(mirna2disease.keys(), mir_targetdb, 'Disease', 'Number of Gene Targets', 'dis_tarnum')
	
	# print 'Number, Disease, Expression'

	# violin_nocomp(mirna2disease.keys(), mir_expdb, 'Disease', 'Number of Tissues Expressed In ', 'dis_tisnum')

	# print 'Number, Family, Targets'

	# violin_nocomp(flatten(mirna2family_edited.values()), mir_targetdb, 'Family', 'Number of Gene Targets', 'fam_tarnum')
	
	# print 'Number, Family, Expression'

	# violin_nocomp([a for a in flatten(mirna2family_edited.values()) if a in mirna2age and mirna2age[a] < 100.0], mir_expdb, 'Family', 'Number of Tissues Expressed In', 'fam_tisnum_young')

	# print 'Hamming, Disease, Targets'

	# violin_comp_norel(mirna2disease.keys(), round_robyn_target, 'Disease', 'Hamming Target Comparisons', 'dis_tarham')

	# print 'Hamming, Disease, Expression'

	# violin_comp_norel(mirna2disease.keys(), round_robyn_exp, 'Disease', 'Hamming Expression Comparisons', 'dis_tisham')

	# print 'Hamming, Family, Targets'

	# violin_comp_norel(flatten(mirna2family_edited.values()), round_robyn_target, 'Family', 'Hamming Target Comparisons', 'fam_tarham')

	# print 'Hamming, Family, Expression'

	# violin_comp_norel(flatten(mirna2family_edited.values()), round_robyn_exp, 'Family', 'Hamming Expression Comparisons', 'fam_tisham')

	# print 'Hamming Related, Family, Targets'

	# violin_comp_rel(mirna2family_edited, round_robyn_target, 'Family', 'Hamming Target Comparisons', 'fam_tarham')

	# print 'Hamming Related, Family, Expression'

	# violin_comp_rel(mirna2family_edited, round_robyn_exp, 'Family', 'Hamming Expression Comparisons', 'fam_tisham')

	violin_comp_rel_ratio(mirna2family_edited, round_robyn_target, 'Family', 'Hamming Target Comparisons', 'fam_tarham', mir_targetdb)


	# print 'Hamming, Family, Expression, Above  15'

	mirna2family_edited_above15 = {}

	for alpha in mirna2family_edited:
		mems = mirna2family_edited[alpha]
		num = [a for a in mems if a in mir_expdb.index and sum(mir_expdb.loc[a].tolist()) > 10]
		if len(num) == 1: continue
		else:
			mirna2family_edited_above15[alpha] = num


 	# violin_comp_rel(mirna2family_edited_above15, round_robyn_exp, 'Family', 'Hamming Expression Comparisons', 'fam_tisham_above15')



mirdb = '../relevant_data/star_mir_lst.txt'
famdb = '../relevant_data/miFam.dat'
diseasedb = '/Users/virpatel/projects/vanderbilt-summer-2014/data/microRNA_disease.txt'
agedb = '../relevant_data/allmir_ages/hsa_family_file_ph_allmir_dollo_age-time.protein_list'
tardb = '../relevant_data/all_targets.txt'
expdb = '../relevant_data/exp_data_alldmir.txt'
taragedb = '../ProteinHistorian/example/ages/human_age-label_dollo.txt'
timetreedb = '../relevant_data/time_tree_dates.txt'


predict_mir_targetdb = pd.read_csv('../relevant_data/mir_predictions_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')
pred_target_hamming = pd.read_csv('../relevant_data/predictions_hamming_target_dataframe.txt', sep='\t',index_col=[0], encoding='utf-8')

mega_mir_lst, mirlst_by_species, human_mirlst = sort_mir(open(mirdb,'r'),open(famdb,'r'))
mirna2age, age2mirna = age_parser(open(agedb, 'r'))
mirna2tar, tar2age = parse_target_data(tardb,taragedb,timetreedb)
gene2age = tar2age.copy()
mirna2family = human_mirlst.copy()



