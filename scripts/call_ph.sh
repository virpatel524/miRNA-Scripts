for fle in "/Users/virpatel/Desktop/pub_stuff/relevant_data/dis2mir_db/*"; do
	if [[ $fle != *'DS_STORE'* ]]; then
		cd /Users/virpatel/Desktop/pub_stuff/ProteinHistorian
		$(python -l /Users/virpatel/Desktop/pub_stuff/relevant_data/time_tree_dates.txt /Users/virpatel/Desktop/pub_stuff/relevant_data/mirna2age_lst.txt $fle)

	fi
done