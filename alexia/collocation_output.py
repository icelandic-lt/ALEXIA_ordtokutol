import glob
from alexia.sql.sql_lookup import SQLDatabase, SQLiteQuery
from progress.bar import IncrementalBar
import sys

def user_defined_collocations(database,filterbase,corpus):
    """
    Iterates through the corpus and retrieves the words that do 
    not appear in the database. Collects 5 word collocations on
    every word, two words before and after the candidate word. 
    """
    db = SQLDatabase(db_name=database)
    txt_files = glob.glob(corpus+'/**/*.txt', recursive=True)
    if filterbase != 'None':
        filters = SQLDatabase(db_name=filterbase)
    else:
        pass    # if there is no filterbase, ignore this step

    outdict = {}
    
    print("""
    ============================================================
    Reading corpus files.
    ============================================================
    """)
    filebar = IncrementalBar('Progress', max = len(txt_files))
    for file in txt_files:
        with open(file, 'r', encoding='utf-8') as content:
            f = content.read()
            words = f.split()
            for i, w in enumerate(words):
                if w[-1] == '-': # if a word starts or ends in an hyphen, ignore it (likely OCR error)
                    continue
                if w[0] == '-':
                    continue
                if (not all(i.isalpha() or i == '-' for i in w)): # if a word contains anything but an alphabetic letter or hyphen, ignore it
                    continue
                if filterbase != 'None': # if a stopword database has been defined, filter the results
                    filter_query = SQLiteQuery(w,'filter','FILTER_WORD_FORMS', cursor=filters.cursor) 
                    if filter_query.exists:
                        continue
                    else:
                        query = SQLiteQuery(w,'word','LEXICON_WORD', cursor = db.cursor) # parameters must be updated if the database format is changed                 
                        query_lower = SQLiteQuery(w.lower(),'word','LEXICON_WORD', cursor = db.cursor) 
                        if not query.exists and not query_lower.exists: # If the word is not found in the database nor the filters 
                            if len(w) > 1: 
                                if i-2 < 0:     # collects 2 words before and after the candidate
                                    w1 = ""
                                else:
                                    w1 = str(words[i-2])
                                if i-1 < 0:
                                    w2 = ""
                                else:
                                    w2 = str(words[i-1])
                                if i+1 > len(words)-1: 
                                    w4 = ""
                                else:
                                    w4 = str(words[i+1])
                                if i+2 > len(words)-1:
                                    w5 = ""
                                else:
                                    w5 = str(words[i+2])
                                if w in outdict:
                                    if str(w1+' '+w2+' '+w+' '+w4+' '+w5) not in outdict[w]['colloc']:
                                        outdict[w]['colloc'][str(w1+' '+w2+' '+w+' '+w4+' '+w5)] = 1
                                    else:
                                        outdict[w]['colloc'][str(w1+' '+w2+' '+w+' '+w4+' '+w5)] += 1
                                    outdict[w]['freq'] += 1
                                else:
                                    outdict[w] = {}
                                    outdict[w]['freq'] = 1
                                    outdict[w]['colloc'] = {str(w1+' '+w2+' '+w+' '+w4+' '+w5): 1}

                else:
                    query = SQLiteQuery(w,'word','LEXICON_WORD', cursor = db.cursor)                 
                    query_lower = SQLiteQuery(w.lower(),'word','LEXICON_WORD', cursor = db.cursor) 
                    if not query.exists and not query_lower.exists: 
                        if len(w) > 1:
                            if i-2 < 0:
                                w1 = ""
                            else:
                                w1 = str(words[i-2])
                            if i-1 < 0:
                                w2 = ""
                            else:
                                w2 = str(words[i-1])
                            if i+1 > len(words)-1: 
                                w4 = ""
                            else:
                                w4 = str(words[i+1])
                            if i+2 > len(words)-1:
                                w5 = ""
                            else:
                                w5 = str(words[i+2])
                            if w in outdict:
                                if str(w1+' '+w2+' '+w+' '+w4+' '+w5) not in outdict[w]['colloc']:
                                    outdict[w]['colloc'][str(w1+' '+w2+' '+w+' '+w4+' '+w5)] = 1
                                else:
                                    outdict[w]['colloc'][str(w1+' '+w2+' '+w+' '+w4+' '+w5)] += 1
                                outdict[w]['freq'] += 1
                            else:
                                outdict[w] = {}
                                outdict[w]['freq'] = 1
                                outdict[w]['colloc'] = {str(w1+' '+w2+' '+w+' '+w4+' '+w5): 1}
                        
        filebar.next()
        sys.stdout.flush()
    filebar.finish()


    output_file = input("""
    ============================================================
    Please indicate what your output file should be called,
    followed by .freq

    Example: lexicon_collocations.freq
    ============================================================
    """)

    with open('output/user_defined/'+output_file, mode='w+') as outputfile:
        candidates = {k: v for k, v in sorted(outdict.items(),
                        key=lambda item: item[1]['freq'], reverse=True)} # Sort the candidates by their total frequencies
        for key, item in candidates.items():    
            for counter, dictitem in enumerate(item.items()):
                if counter % 2 == 0:
                    freq = dictitem[1]
                elif counter % 2 != 0:
                    sorted_sents = {k: v for k, v in sorted(dictitem[1].items(), # Sort the sentence examples by their frequencies
                        key=lambda item: item[1], reverse=True)}
                    if len(sorted_sents) > 5:   # This limit the examples to the 5 most frequent ones, can be changed
                        sents = list(sorted_sents)[:5]
                    else:
                        sents = list(sorted_sents)
                    outputfile.write(key+' : '+str(freq)+'. '+str(sents)+'\n') # word: freq. [sent example 1, sent example 2...]

    print(f"""
    ============================================================
    Output file {output_file} is ready and can be 
    found at the output/user_defined/ directory.
    ============================================================
    """)