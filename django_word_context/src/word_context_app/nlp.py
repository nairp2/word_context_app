import pandas as pd
import spacy
import numpy as np
from spacy.language import Language
import os
import docx2txt
import warnings
warnings.filterwarnings("ignore")
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words("english"))

def all_file_paths(master_directory):

    path_l = []
    for root, dirs, files in os.walk(master_directory):
        if files:
            for i in files:
                path = os.path.join(root, i)
                path = path.replace(os.path.sep, '/')

                if path == 'bbc_doc/desktop.ini': # exlcude files and move it to settings.
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

    # wordfreq = []
    # for w in tokens_str:
    #     wordfreq.append(tokens_str.count(w))
    #
    #
    # for i in list(zip(tokens_str, wordfreq)):
    #     if query == i[0]:
    #         word_occurences = (i[0], i[1])
    #         break
    #
    # line = 0
    # word_not_found = []
    #
    # for word in text:
    #     if word == '\n':
    #         line += 1

    doc_list = text.lower().splitlines()
    doc_list = [i for i in doc_list if i]

    return doc_list

def sim_word(query, path, score):

#FI
    text = docx2txt.process(path)
    string_txt = str(text)

    nlp = spacy.load('en_core_web_lg',disable = ['ner', 'parser'])
    nlp.Defaults.stop_words -= {
'about',
'above',
'across',
'after',
'afterwards',
'again',
'against',
'all',
'almost',
'alone',
'along',
'already',
'always',
'amount',
'anyhow',
'anyone',
'anything',
'anyway',
'anywhere',
'became',
'because',
'become',
'becomes',
'becoming',
'before',
'beforehand',
'behind',
'being',
'below',
'beside',
'besides',
'between',
'beyond',
'both',
'bottom',
'doing',
'done',
'down',
'due',
'during',
'each',
'eight',
'either',
'eleven',
'else',
'elsewhere',
'empty',
'enough',
'even',
'ever',
'every',
'everyone',
'everything',
'everywhere',
'except',
'few',
'fifteen',
'fifty',
'first',
'five',
'former',
'formerly',
'forty',
'four',
'from',
'front',
'full',
'further',
'get',
'give',
'go',
'here',
'hereafter',
'hereby',
'herein',
'hereupon',
'how',
'hundred',
'indeed',
'itself',
'just',
'keep',
'last',
'latter',
'latterly',
'least',
'less',
'made',
'make',
'many',
'may',
'meanwhile',
'might',
'mine',
'more',
'moreover',
'most',
'mostly',
'move',
'much',
'must',
'myself',
'name',
'namely',
'neither',
'never',
'nevertheless',
'next',
'nine',
'nobody',
'none',
'noone',
'not',
'nothing',
'now',
'nowhere',
'often',
'one',
'only',

'other',
'others',
'otherwise',

'ourselves',
'out',
'over',
'own',
'part',
'per',
'perhaps',
'please',
'quite',
'rather',
'really',
'regarding',
'same',
'say',
'see',
'seem',
'seemed',
'seeming',
'seems',
'serious',
'several',
'should',
'show',
'side',
'since',
'six',
'sixty',
'some',
'somehow',
'someone',
'something',
'sometime',
'sometimes',
'somewhere',
'still',
'such',

'ten',



'third',


'three',


'together',

'top',

'twelve',
'twenty',
'two',
'under',
'unless',

'used',
'using',
'various',
'very',
'well',


'whatever',
'when',
'whence',
'whenever',
'where',
'whereafter',

'whereby',
'wherein',
'whereupon',
'wherever',
'whether',
'which',
'while',
'whither',
'who',
'whoever',
'whole',
'within',
'without',

}
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS


    tokens = nlp(text)
    lemma_list = []
    for token in tokens:
        if token.is_stop is False:
            token_preprocessed = preprocessor(token.text)
            if token_preprocessed != '':
                 lemma_list.append(nlp(token_preprocessed))


    tokens_str = text.lower()
    tokens_str = word_tokenize(tokens_str)
    tokens_str = [i for i in tokens_str if not i in nlp.Defaults.stop_words]
    #print(token)
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
    paragraph_matrix_list = []

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

    for i,j in enumerate(lemma_list):
           if str(j.text[-1]) == 's' and j[0].tag_ == 'NNS':

               j = str(j.text[:-1])

               lemma_list[i] = nlp(j)

    for i in lemma_list:




        s = key.similarity(i)

        if s >= score:
            words.append(i.text)

            # PN
            sim_score.append(s)





            word_found_lines, line_list = findline(str(i.text),doc_list)
            #print(line_list)
            l_line_list = []
            l_line_list.append(tuple(line_list))
            paragraph_lines = list(line_list)
            #paragraph_lines = [ele for ele in paragraph_lines if ele != []]
            word_count.append(round(len(word_found_lines), 0))

            pg_list.append(tuple(word_found_lines))
            line_list_words.append(tuple(line_list))

    word_count = np.around(np.array(word_count),0)

    sim_score = np.around(np.array(sim_score),2)

    matrix = pd.DataFrame({'Words': words, 'Similarity_Score': sim_score,'Paragraph_Numbers': pg_list, 'Count': word_count, 'Paragraphs': line_list_words, 'Path': path}, index = words)

    #matrix = pd.DataFrame({'Similarity Score': sim_score,'Paragraph Numbers': pg_list, 'Count': word_count}, index = words)
    matrix = matrix.drop_duplicates()

    matrix =  matrix.sort_values(by=['Similarity_Score'],ascending=False)
    #print("For document: {}, path: {}, keyword: {}, Similarity Score Threshold: {}".format(os.path.basename(path),path,query,score))
    #print(matrix)
    return matrix
   # print('\n')


def nlp_query(query, root, sim_score):

    nlp = spacy.load('en_core_web_lg',disable = ['ner', 'parser'])
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
    #print(nlp.pipe_names)
    if not os.path.exists('Index'):
       os.makedirs('Index')

    if os.path.exists('Index/{}_{}_{}.csv'.format(query, root.replace("/","_"), sim_score)):
       df = pd.read_csv('Index/{}_{}_{}.csv'.format(query, root.replace("/","_"), sim_score))
       df = df.fillna('')
       return df

    all_path = all_file_paths(root) # change to root
    #print(all_path)

    #for i in all_path:
    #    print(i)

    #sim_word(path,query,score)

    df = pd.DataFrame()
    # final_df = []

    for i in all_path:
        print(i)
        output = sim_word(query, i, score=sim_score)
        output = output[output.Count != 0]
        output = output.explode(['Paragraphs', 'Paragraph_Numbers'])
        output.loc[(output['Words'].duplicated() & output['Similarity_Score'].duplicated() & output['Count'].duplicated() & output['Path'].duplicated()), ['Words', 'Similarity_Score', 'Count', 'Path']] = ''
        df = pd.concat([df, output])
        #word_df.append(output)
    #word_df = [df for df in word_df if not df.empty]
    #word_df = word_df[word_df.Count != 0]
    #df = pd.concat(word_df)
    #print(df)
    #df = df.explode(['Paragraphs', 'Paragraph_Numbers'])
    #df.loc[(word_df['Words'].duplicated() & word_df['Similarity_Score'].duplicated() & word_df['Count'].duplicated()), ['Words', 'Similarity_Score', 'Count']] = ''
    #output = output[output.Count != 0]
    #output = output.explode(['Paragraphs', 'Paragraph_Numbers'])
    #output.loc[(output['Words'].duplicated() & output['Similarity_Score'].duplicated() & output['Count'].duplicated()), ['Words', 'Similarity_Score', 'Count']] = ''
    #if sim_score == 1.0:
    #    output = output[output.Similarity_Score == 1.0]
    #word_df = [df for df in word_df if not df.empty] # removing dataframes that are empty
    # dropping rows with Count having a value of 0
    #for df in word_df:
    #    df = df[df.Count != 0]
    #    final_df.append(df)
    # Check unigram,bigram, web app interface, check time complexity with 300 pages dataset, similar to google search from 1-100(access index of dataframe list: click 1 will trigger i-1 index of list)

    #print(final_df)

    #df = pd.concat(final_df)
    #print("Word df:")
    #print(word_df)
    #print("Final df:")
    #print(df)

    df.to_csv("Index/{}_{}_{}.csv".format(query, root.replace("/","_"), sim_score), index=False)
    #output = df
    #json = {'output': final_df[0]}
    return df
