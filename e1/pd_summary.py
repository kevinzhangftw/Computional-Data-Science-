
# coding: utf-8

# In[63]:

import pandas as pd


# In[64]:

totals = pd.read_csv('totals.csv').set_index(keys=['name'])


# In[65]:

print(totals)


# In[66]:

counts = pd.read_csv('counts.csv').set_index(keys=['name'])


# In[67]:

print(counts)


# In[68]:

totalsSum = pd.DataFrame.sum(totals, axis=1)


# In[69]:

print(totalsSum)


# In[70]:

lowestPrecipitation = pd.Series.argmin(totalsSum)


# In[71]:

print(lowestPrecipitation)


# In[72]:

precipitationTotal = pd.DataFrame.sum(totals, axis=0)


# In[73]:

monthlyCountsTotal = pd.DataFrame.sum(counts, axis=0)


# In[74]:

averagePrecipitation = precipitationTotal / monthlyCountsTotal


# In[76]:

print(averagePrecipitation)


# In[78]:

countsSum = pd.DataFrame.sum(counts, axis=1)


# In[82]:

cityAveragePrecipitation = totalsSum / countsSum


# In[83]:

print(cityAveragePrecipitation)


# In[ ]:



