import csv

with open('../raw_data/Predicted_Targets_Info.default_predictions.txt','r') as predictions_fle:
	data = list(csv.reader(predictions_fle, delimiter='\t'))[1:]

target_lst = []

for alpha in data:
	mir = alpha[0].lower()
	if '3p' in mir or '5p' in mir:
		tmp = mir.split('-')
		new_name = 'hsa-' + '-'.join(tmp[:-1])
	else:
		new_name = 'hsa-' + mir
	mir = new_name
	gene = alpha[2]
	target_lst.append([mir,gene])

with open('../relevant_data/target_predictions_targetscan.txt','w') as predictions_write:
	for alpha in target_lst:
		predictions_write.write('%s\t%s\n' %(alpha[0], alpha[1]))


