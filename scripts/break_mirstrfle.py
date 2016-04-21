import csv


file = open('/Users/virpatel/Desktop/miRNA.str','r')
mir_list_embl = csv.reader(file) 

all_mir_lst = []
select_mir_lst = []

for i in mir_list_embl:
	if i == []: continue
	if i[0][0] != '>': continue
	temp = [alpha for alpha in i[0].split(' ') if alpha != '' and i[0][0] == '>']
	mirname = temp[0][1:]
	energy = temp[1]
	if len(temp) == 3: all_mir_lst.append(mirname)
	else:
		all_mir_lst.append(mirname)
		select_mir_lst.append(mirname)


all_fle = open('/Users/virpatel/Desktop/pub_stuff/relevant_data/all_mir_lst.txt','w')
str_fle = open('/Users/virpatel/Desktop/pub_stuff/relevant_data/select_data_lst.txt','w')


for i in all_mir_lst:
	all_fle.write(i + '\n')


for i in select_mir_lst:
	str_fle.write(i + '\n')

all_fle.close()
str_fle.close()







	