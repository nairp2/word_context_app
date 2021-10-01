#!/usr/bin/env python
# coding: utf-8

# In[10]:

from similarity_score_functions import all_file_paths
from similarity_score_functions import preprocessor
from similarity_score_functions import findline
from similarity_score_functions import word_occurences
from similarity_score_functions import sim_word
from similarity_score_functions import nlp_query

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)
pd.set_option("max_rows", None)

import time



# In[10]:

import sys

    
# var = sys.argv

# query = var[1]
# directory = var[2]



# In[10]:
    
# start = time.time()

# output = sim_word("bbc_doc//business//001.docx",query,0.6)

# if output.empty:
#     print('\n')
#     print("Query - '{}' and similar words \nnot found in file path - {}".format(query,i))
#     print("------------------------------------------------")
# else:
#     output = output[output.Count != 0]
    
#     print('\n')
#     print("Query - '{}'".format(query))
#     print("file path - {}".format(i))
#     print(output)
#     print("------------------------------------------------")
    
# end = time.time()

# print("time",end - start)




    
# In[10]:
start = time.time()
x = nlp_query("profit", "bbc_doc", 0.55)
end = time.time()

print("time",end - start)



















