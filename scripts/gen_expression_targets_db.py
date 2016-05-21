import csv 


starting_targets = '/Users/virpatel/Desktop/hsa_targets.txt'
starting_exp = '/Users/virpatel/Desktop/mirmine.txt'

mir2targets = {}
mir2bool_exp = {}

tissue_simplifier = {}
simp_key = []

with open(starting_targets,'r') as starting_targets_fle:
	parsed = list(csv.reader(starting_targets_fle,delimiter='\t'))
	for mir in parsed:
		if mir[1][:3] != 'hsa':
			continue
		if '-3p' in mir[1] or '-5p' in mir[1] :
			mir2targets.setdefault(mir[1][:-3].lower(),[]).append(mir[3])
		else:
			mir2targets.setdefault(mir[1].lower(),[]).append(mir[3])
	for mir in mir2targets:
		mir2targets[mir] = list(set(mir2targets[mir]))

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/all_targets.txt','w') as targets_db_fle:
	for mir in mir2targets:
		for tar in mir2targets[mir]:
			targets_db_fle.write('%s\t%s\n' %(mir, tar))




with open(starting_exp) as starting_exp_fle:
	parsed = list(csv.reader(starting_exp_fle,delimiter='\t'))



	for s in parsed[0][1:]:
		 simp_key.append(s[s.find("(")+1:s.find(")")])


	simp_key = list(set(simp_key))

	for index, s in enumerate(parsed[0][1:]):
		 cur_tis = s[s.find("(")+1:s.find(")")]
		 tissue_simplifier[index] = simp_key.index(cur_tis)


	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/tissue_matrix.txt','w') as tis_mat_fle:
		for alpha in simp_key:
			tis_mat_fle.write('%s\n' %(alpha))




	for mir in parsed[1:]:
		if '-3p' in mir[0] or '-5p' in mir[0]:
			mir_base = mir[0][:-3].lower()
		else: 
			mir_base = mir[0].lower()
		if mir_base in mir2bool_exp:
			for index, exp in enumerate(mir[1:]):
				new_exp = float(exp)
				if new_exp > 0: 
					if mir2bool_exp[mir_base][tissue_simplifier[index]] == 0: mir2bool_exp[mir_base][tissue_simplifier[index]] = 1
		else:
			newlst = [0] * len(simp_key)
			for index, exp in enumerate(mir[1:]):
				new_exp = float(exp)
				if new_exp > 0: newlst[tissue_simplifier[index]] = 1
			mir2bool_exp[mir_base] = newlst

	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt','w') as exp_all_fle:
		for mir in mir2bool_exp:
			exp_all_fle.write('%s\t' %(mir))
			for index,val in enumerate(mir2bool_exp[mir]):
				if index == len(mir2bool_exp[mir]) - 1:
					exp_all_fle.write('%i\n' %(val))
				else:
					exp_all_fle.write('%i\t' %(val))












	
