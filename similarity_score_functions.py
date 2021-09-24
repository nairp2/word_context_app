#!/usr/bin/env python
# coding: utf-8

# In[10]:


import spacy
from spacy.language import Language
import os
import ntpath
from pathlib import Path

import docx2txt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 50)
pd.set_option("max_rows", None)
import warnings
warnings.filterwarnings("ignore")
import re


# In[11]:


nlp = spacy.load('en_core_web_lg',disable = ['ner', 'parser'])
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS


# In[12]:


import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words("english"))


# In[ ]:



# In[13]:


def all_file_paths(master_directory):   
    
    path_l = []
    for root, dirs, files in os.walk(master_directory):
        
        

        if files:
            for i in files:
                path = os.path.join(root, i)
                path = path.replace(os.path.sep, '/')

                if path == 'bbc_doc/desktop.ini':
                    continue
                path_l.append(path)
                
    
    return(path_l)



# In[21]:
    
all_path = all_file_paths("bbc_doc")

print(all_path[0])



# In[10]:    
    
print(sim_word("bbc_doc//business//001.docx","profit",0.6))

# In[10]:  
print(sim_word("bbc_doc\\business\\001.docx","profit",0.6))


# In[21]:


def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    text = re.sub('[\W]+', '', text.lower())
    return text


def findline(word,doc_list): #Added doc_list as var
    line_num = []
    line_list = []
    for i in range(len(doc_list)):
        if word in doc_list[i]:
            line_num.append(i+1)
            line_list.append(doc_list[i])

    return line_num, line_list


def word_occurences(text, tokens_str, query):
    

    doc_list = text.lower().splitlines()
    doc_list = [i for i in doc_list if i]
    
    return doc_list





# In[28]:


def sim_word(path,query,score):
 
#FI
    text = docx2txt.process(path)
    string_txt = str(text)

    tokens = nlp(text)
    lemma_list = []
    for token in tokens:
        if token.is_stop is False:
            token_preprocessed = preprocessor(token.text)
            if token_preprocessed != '':
                 lemma_list.append(nlp(token_preprocessed))
   
  
#FI    
    
    query = query
    
    l_q = len(nlp(query))
    
    if l_q >= 2:
        
        bi_g = []
        c=0
        while c < len(lemma_list)-1:

            bi_g.append(nlp(lemma_list[c].text+" "+lemma_list[c+1].text))
            c = c+1


        lemma_list = lemma_list+bi_g
    
#PN 
    doc_list = word_occurences(text, lemma_list, query)
    

    paragraph_list = []
    
    string_list = string_txt.splitlines()
    
    for word in string_list:
        if word != '':
            paragraph_list.append(word)

#PN


#FI & PN
    key = nlp(query)
    
    sim_score = []
    words = []
    word_count = []


    pg_list = []
    line_list_words = []

    for i in lemma_list:
        s = key.similarity(i)

        if s >= score:
            words.append(i)
                
            # PN
            
            word_found_lines, line_list = findline(str(i.text),doc_list)


            word_count.append(len(word_found_lines))
            
            pg_list.append(tuple(word_found_lines))
            line_list_words.append(tuple(line_list))
            sim_score.append(s)
    
    matrix = pd.DataFrame({'Similarity Score': sim_score,'Paragraph Numbers': pg_list, 'Count': word_count, 'Paragraphs': line_list_words}, index = words)

    matrix = matrix.drop_duplicates()

    matrix =  matrix.sort_values(by=['Similarity Score'],ascending=False)
    matrix = matrix[matrix.Count != 0]

    return matrix


#FI & PN


# In[30]:

# all_path = all_file_paths("bbc_doc")

# for i in all_path:
#     print(i)
    
# In[30]:


# Check unigram,bigram, web app interface, check time complexity with 300 pages dataset, similar to google search from 1-100(access index of dataframe list: click 1 will trigger i-1 index of list)
# print('\n')
# print("ONE")
# print("ONE")
# print("ONE")

# for i in all_path[:]:
#     output = sim_word(i,query,0.6)
    
#     if output.empty:
#         print('\n')
#         print("Query - '{}' and similar words \nnot found in file path - {}".format(query,i))
#         print("------------------------------------------------")
#     else:
#         output = output[output.Count != 0]
        
#         print('\n')
#         print("Query - '{}'".format(query))
#         print("file path - {}".format(i))
#         print(output)
#         print("------------------------------------------------")

    
# # In[30]:
        
# print("ALL")
# print("ALL")
# print("ALL")

# for i in all_path[:]:
#     output = sim_word(i,"profit",0.6)
    
#     if output.empty:
#         print('\n')
#         print("Query - '{}' and similar words \nnot found in file path - {}".format(query,i))
#         print("------------------------------------------------")
        
#     else:
#         output = output[output.Count != 0]
        
#         print('\n')
#         print("Query - {}".format(query))
#         print("file path - {}".format(i))
#         print(output)
#         print("------------------------------------------------")




# In[8]:


# l = ["at1","at2","at3","at4"]
# l2 = []
# l3 = []
# l4 = []

# i=0
# while i < len(l)-1:
#     print(i)
#     l2.append(l[i]+" "+l[i+1])
#     i = i+1
    
# i=0
# while i < len(l)-2:
#     print(i)
#     l3.append(l[i]+" "+l[i+1]+" "+l[i+2])
#     i = i+1

# i=0
# while i < len(l)-3:
#     print(i)
#     l4.append(l[i]+" "+l[i+1]+" "+l[i+2]+" "+l[i+3])
#     i = i+1
    
# l + l2 + l3 + l4


# In[ ]:


# if word_found_lines:
#     pass
# else:
#     continue


# ### Trying with transformer models 

# In[9]:


# from sentence_transformers import SentenceTransformer, util
# import numpy as np

# model = SentenceTransformer('stsb-roberta-large')

# sentence1 = "Word"
# sentence2 = "Word"
# # encode sentences to get their embeddings
# embedding1 = model.encode(sentence1, convert_to_tensor=True)
# embedding2 = model.encode(sentence2, convert_to_tensor=True)
# # compute similarity scores of two embeddings
# cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
# print("Sentence 1:", sentence1)
# print("Sentence 2:", sentence2)
# print("Similarity score:", cosine_scores.item())


# key = "learn"

# embedding1 = model.encode(key, convert_to_tensor=True)

# for i in lemma_list:
#     i = i.text
     
#     embedding2 = model.encode(i, convert_to_tensor=True)
#     # compute similarity scores of two embeddings
#     cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    
#     if cosine_scores > 0.5:
#         print("Key:{} \nWord Found:{} \nSimilarity score:{:0.2f}".format(key,i,np.array(cosine_scores)[0][0]))
#         print("----------------------------------------------------")  


# In[ ]:


# def sim_word(path,query,score=0.6):
 
# #FI
#     text = docx2txt.process(path)
#     string_txt = str(text)


#     tokens = nlp(text)
#     lemma_list = []
#     for token in tokens:
#         if token.is_stop is False:
#             token_preprocessed = preprocessor(token.text)
#             if token_preprocessed != '':
#                  lemma_list.append(nlp(token_preprocessed))
   

# #     tokens_str = text.lower()
# #     tokens_str = word_tokenize(tokens_str)
# #     tokens_str = [i for i in tokens_str if not i in stop_words]  
    

    
#     l_q = len(nlp(query))
    
#     if l_q >= 2:
        
#         bi_g = []
#         c=0
#         while c < len(lemma_list)-1:

#             bi_g.append(nlp(lemma_list[c].text+" "+lemma_list[c+1].text))
#             c = c+1


#         lemma_list = lemma_list+bi_g
    

    
    
    
# #PN    
#     doc_list = word_occurences(text, lemma_list, query)
    
#     string_list = []
#     paragraph_list = []
#     paragraph_matrix_list = []
    
#     string_list.append(string_txt)
    
#     string_list = string_list[0].splitlines()
    
#     for word in string_list:
#         if word != '':
#             paragraph_list.append(word)

# #PN


# #FI & PN
#     key = nlp(query)
    
#     sim_score = []
#     words = []
#     word_count = []

#     pg_list = []
#     line_list_words = []


#     for i in lemma_list:
#         s = key.similarity(i)

#         if s > score:
#             words.append(i)
                
#             # PN
#             sim_score.append(s)
            
#             word_found_list = []
#             word_found_list.append(str(i.text))
#             word_found_lines,line_list = findline(word_found_list[0],doc_list)
            
#             if word_found_lines:
#                 pass
#             else:
#                 continue

#             l_line_list = []
#             l_line_list.append(tuple(line_list))
#             paragraph_lines = list(line_list)
#             #paragraph_lines = [ele for ele in paragraph_lines if ele != []]
#             word_count.append(len(word_found_lines))
            
#             pg_list.append(tuple(word_found_lines))
#             words.append(i)
#             sim_score.append(s)
            

#     matrix = pd.DataFrame({'Similarity Score': sim_score,'Paragraph Numbers': pg_list, 'Count': word_count, 'Paragraphs': line_list_words, 'Path': path}, index = words)

#     #matrix = pd.DataFrame({'Similarity Score': sim_score,'Paragraph Numbers': pg_list, 'Count': word_count}, index = words)
#     matrix = matrix.drop_duplicates()

#     matrix =  matrix.sort_values(by=['Similarity Score'],ascending=False)
#     #print("For document: {}, path: {}, keyword: {}, Similarity Score Threshold: {}".format(os.path.basename(path),path,query,score))
#     #print(matrix)
#     return matrix

# #FI & PN


# In[ ]:





# In[ ]:




