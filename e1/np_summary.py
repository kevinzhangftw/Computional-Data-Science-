
# coding: utf-8

# In[165]:

import numpy as np


# In[166]:

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']


# In[167]:

sum = np.sum(totals, axis=1)


# In[168]:

cityLowest = np.argmin(sum)


# In[169]:

print(cityLowest)


# In[170]:

totalPrecipitation = np.sum(totals, axis=0)


# In[171]:

totalObservations = np.sum(counts, axis=0)


# In[172]:

averagePrecipitation = totalPrecipitation / totalObservations


# In[173]:

print(averagePrecipitation)


# In[174]:

countSum = np.sum(counts, axis=1)


# In[175]:

cityPrecipitation = sum/countSum


# In[176]:

print(cityPrecipitation)


# In[177]:

quarters = np.reshape(totals, (9,4,3))


# In[178]:

quartersSum = np.sum(quarters, axis=2)


# In[179]:

print(quartersSum)


# In[ ]:




# In[ ]:



