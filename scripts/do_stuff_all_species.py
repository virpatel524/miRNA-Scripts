import os
import pandas as pd
from scipy.stats import spearmanr, skew
import matplotlib.pyplot as plt
import seaborn as sns
import csv

sns.axes_style('whitegrid')
sns.set_style("whitegrid")
sns.set_context("paper")


species2agedata = {}

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/ph_dataset_with_time_tree_allmir.txt') as master_age_mirlst:
	mirlst = list(csv.reader(master_age_mirlst,delimiter='\t'))
	for mir in mirlst:
		spe = mir[0][:3]
		species2agedata.setdefault(spe,[]).append(float(mir[-1]))





specieslst = []
skewlst = []
percentlst = []
num_mir = []

for species in species2agedata:
	tmp_data = sorted(species2agedata[species][:])

	if len(list(set(tmp_data))) < 5: continue

	specieslst.append(species)
	skewlst.append(float(skew(species2agedata[species])))

	tmp_data = sorted(species2agedata[species][:])
	num_lowest = float(len([p for p in tmp_data if p == tmp_data[0]]))
	percentlst.append(num_lowest/float(len(tmp_data)))
	num_mir.append(float(len(tmp_data)))







alldata = pd.DataFrame({'species': specieslst, 'skew_vals': skewlst, 'per_lowest': percentlst, 'num_mir': num_mir})

print spearmanr(alldata['per_lowest'], alldata['num_mir'])


plt.gcf().set_size_inches(20, 10)
sns.regplot(alldata['num_mir'], alldata['skew_vals'],fit_reg=False)
plt.xlim([-1,1100])
plt.ylim(-.4)
plt.xlabel('Number of Annotated miRNAs per Species',fontsize=17)
plt.ylabel('Skewness of Species miRNA Age Distribution',fontsize=17)


plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/allspec_skewness.pdf',bbox_inches='tight'g)
plt.close()

plt.gcf().set_size_inches(20, 10)
sns.regplot(alldata['num_mir'], alldata['per_lowest'],fit_reg=False)
plt.xlabel('Number of Annotated miRNAs per Species',fontsize=17)
plt.ylabel('Perecentage of miRNAs with Earliest Origin',fontsize=17)
plt.xlim([-1,1100])
plt.ylim(-.001)
plt.show()
plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/allspec_percent.pdf',bbox_inches='tight')
plt.close()



