#!/usr/bin/env python
# coding: utf-8

# In[10]:

from similarity_score_functions import all_file_paths
from similarity_score_functions import preprocessor
from similarity_score_functions import findline
from similarity_score_functions import word_occurences
from similarity_score_functions import sim_word

import time



# In[10]:

import sys

    
# var = sys.argv

# query = var[1]
# directory = var[2]

query = "profit"

# In[10]:


all_path = all_file_paths("bbc_doc")

for i in all_path:
    print(i)
    
# In[10]:
start = time.time()

output = sim_word("bbc_doc/business/001.docx",query,0.6)

if output.empty:
    print('\n')
    print("Query - '{}' and similar words \nnot found in file path - {}".format(query,i))
    print("------------------------------------------------")
else:
    output = output[output.Count != 0]
    
    print('\n')
    print("Query - '{}'".format(query))
    print("file path - {}".format(i))
    print(output)
    print("------------------------------------------------")
    
end = time.time()

print("time",end - start)

    
# In[10]:

start = time.time()

for i in all_path:
    output = sim_word("bbc_doc/business/001.docx",query,0.6)
    
    if output.empty:
        print('\n')
        print("Query - '{}' and similar words \nnot found in file path - {}".format(query,i))
        print("------------------------------------------------")
    else:
        output = output[output.Count != 0]
        
        print('\n')
        print("Query - '{}'".format(query))
        print("file path - {}".format(i))
        print(output)
        print("------------------------------------------------")
    
end = time.time()
print("time",end - start)
    
# In[10]:

    






def sq(x):
    print(x**2)
    
    




    
# In[10]:

x = 2


sq(x)





















