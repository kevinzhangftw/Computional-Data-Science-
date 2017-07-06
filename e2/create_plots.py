import sys
import pandas as pd
import matplotlib.pyplot as plt

# help from http://stackoverflow.com/questions/18062135/combining-two-series-into-a-dataframe-in-pandas

filename1 = sys.argv[1]
filename2 = sys.argv[2]
table1 = pd.read_table(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])
table2 = pd.read_table(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

stable1 = table1.sort_values(by='views', ascending=False)
stable2 = table2.sort_values(by='views', ascending=False)

s1 = stable1['views']
s2 = stable2['views']
joinedTable = pd.DataFrame(dict(day1 = s1, day2 = s2)).reset_index()

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.title('popularity distribution')
plt.xlabel('views')
plt.ylabel('rank')
plt.axis([0, 2500, 0, 180])
plt.plot(stable1['views'].values)
plt.subplot(1, 2, 2) # ... and then select the second
plt.title('Daily Correlation')
plt.xlabel('day1 views')
plt.ylabel('day2 views')
plt.plot(joinedTable['day1'].values, joinedTable['day2'].values, 'ro')
plt.xscale('log')
plt.yscale('log')
plt.savefig('wikipedia.png')
