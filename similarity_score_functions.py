import pandas as pd
import spacy
import numpy as np
from spacy.language import Language
import os
import docx2txt
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)
pd.set_option("max_rows", None)
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words("english"))

#%%
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

def sim_word(path,query,score):

#FI
    text = docx2txt.process(path)
    string_txt = str(text)

    nlp = spacy.load('en_core_web_lg',disable = ['ner', 'parser'])
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

    tokens = nlp(text)
    lemma_list = []
    for token in tokens:
        if token.is_stop is False:
            token_preprocessed = preprocessor(token.text)
            
            if token_preprocessed != '':
                # if token_preprocessed[-1] == 's':
                #     token_preprocessed = token_preprocessed[:-1]
                    lemma_list.append(nlp(token_preprocessed))
            
            
                



    tokens_str = text.lower()
    tokens_str = word_tokenize(tokens_str)
    tokens_str = [i for i in tokens_str if not i in stop_words]
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

    # string_list = []
    paragraph_list = []
  

    # string_list.append(string_txt)
    #
    # string_list = string_list[0].splitlines()

    string_list = string_txt.splitlines()

    for word in string_list:
        if word != '':
            paragraph_list.append(word)

    #print(paragraph_list)
#PN


#FI & PN
    key = nlp(query)

    sim_score = []
    words = []
    word_count = []
    #paragraph_word_set = set()
   # paragraph_sentences = []

    pg_list = []
    line_list_words = []
    
    pth = []
    
    for i,j in enumerate(lemma_list):
        if str(j.text[-1]) == 's':

            j = str(j.text[:-1])

            lemma_list[i] = nlp(j)
        

    for i in lemma_list:
    
        
        
        s = key.similarity(i)
        

        if s >= score:
            
            words.append(i.text)

            # PN
            sim_score.append(s)
            


            word_found_lines, line_list = findline(str(i.text),doc_list)

            word_count.append(len(word_found_lines))

            pg_list.append(tuple(word_found_lines))
            
            line_list_words.append(tuple(line_list))
            
            pth.append(path)

    sim_score = np.around(np.array(sim_score),2)

    matrix = pd.DataFrame({'Words': words, 'Similarity_Score': sim_score,'Paragraph_Numbers': pg_list, 'Count': word_count, 'Paragraphs': line_list_words,'Path': pth}, index = words)

    #matrix = pd.DataFrame({'Similarity Score': sim_score,'Paragraph Numbers': pg_list, 'Count': word_count}, index = words)
    matrix = matrix.drop_duplicates()

    matrix =  matrix.sort_values(by=['Similarity_Score'],ascending=False)
    #print("For document: {}, path: {}, keyword: {}, Similarity Score Threshold: {}".format(os.path.basename(path),path,query,score))
    #print(matrix)
    return matrix
   # print('\n')


def nlp_query(query, master_directory, sim_score):

    nlp = spacy.load('en_core_web_lg',disable = ['ner', 'parser'])
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
    #print(nlp.pipe_names)
    if not os.path.exists('Index'):
        os.makedirs('Index')
    
    if os.path.exists('Index/{}_{}_{}.csv'.format(query, master_directory.replace("/","_"), sim_score)):
        df1 = pd.read_csv('Index/{}_{}_{}.csv'.format(query, master_directory.replace("/","_"), sim_score))
        df1 = df1.fillna('')
        return df1
    
    
    df1 = pd.DataFrame()
    
    
    
    for i in all_file_paths(master_directory):
        
        print(i)

        output = sim_word(i,query, score=sim_score)
    
        output = output[output.Count != 0]
        output = output.explode(['Paragraphs', 'Paragraph_Numbers'])
        output.loc[(output['Words'].duplicated() & output['Similarity_Score'].duplicated() & output['Count'].duplicated()), ['Words', 'Similarity_Score', 'Count']] = ''
        df1 = pd.concat([df1, output])
        
    df1.to_csv("Index/{}_{}_{}.csv".format(query, master_directory.replace("/","_"), sim_score), index=False)

    return df1