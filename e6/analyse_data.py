from scipy import stats
import pandas as pd
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import sys
import matplotlib.pyplot as plt

data = pd.read_csv(sys.argv[1])
qs1 = data['qs1']
qs2 = data['qs2']
qs3 = data['qs3']
qs4 = data['qs4']
qs5 = data['qs5']
merge1 = data['merge1']
partition_sort = data['partition_sort']

anova = stats.f_oneway(qs1, qs2, qs3, qs4, qs5, merge1, partition_sort)
print(anova)
print('anova pvalue:',anova.pvalue)

dataMelt = pd.melt(data)
posthoc = pairwise_tukeyhsd(
    dataMelt['value'], dataMelt['variable'],
    alpha=0.05)
print(posthoc)

fig = posthoc.plot_simultaneous()
fig.set_size_inches((5, 2))
plt.show()
