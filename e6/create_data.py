import time
import numpy as np 
import pandas as pd
from implementations import all_implementations

qs1data = np.array([])
qs2data = np.array([])
qs3data = np.array([])
qs4data = np.array([])
qs5data = np.array([])
merge1data = np.array([])
partition_sortdata = np.array([])

for x in range(1,1400):
	random_array = np.random.randint(1000000, size=x)

	for sort in all_implementations:
	    st = time.time()
	    res = sort(random_array)
	    en = time.time()

	    if (sort == all_implementations[0]):
	    	qs1data = np.append(qs1data, (en - st))
	    if (sort == all_implementations[1]):
	     	qs2data = np.append(qs2data, (en - st))
	    if (sort == all_implementations[2]):
	     	qs3data = np.append(qs3data, (en - st)) 
	    if (sort == all_implementations[3]):
	     	qs4data = np.append(qs4data, (en - st))
	    if (sort == all_implementations[4]):
	     	qs5data = np.append(qs5data, (en - st))
	    if (sort == all_implementations[5]):
	     	merge1data = np.append(merge1data, (en - st))
	    if (sort == all_implementations[6]):
	     	partition_sortdata = np.append(partition_sortdata, (en - st))


columnNames = ['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort']
qs1series = pd.Series(qs1data)
qs2series = pd.Series(qs2data)
qs3series = pd.Series(qs3data)
qs4series = pd.Series(qs4data)
qs5series = pd.Series(qs5data)
merge1series = pd.Series(merge1data)
partition_sortseries = pd.Series(partition_sortdata)

data = pd.concat([qs1series, qs2series, qs3series, 
	qs4series, qs5series, merge1series, 
	partition_sortseries], axis=1)
data.columns = columnNames

# print(data)
data.to_csv('data.csv', index=False)
