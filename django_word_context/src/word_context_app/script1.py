from word_context_app import nlp

#def script_load_paths():
#    all_path = nlp.all_file_paths('bbc_doc') # TODO: all_file_path parameter passed automatically
#    return all_path

def script_select_paths(query, root, score):
    df = nlp.nlp_query(query, root, score)
    word_not_found = str()
    if df.empty:
        word_not_found = "Word not found!"
    #final_df = df[df["Path"] == path]
    #print(df.Path)
    return df, word_not_found
