from xml.etree import ElementTree as ET
from string import punctuation
import glob
from alexia.sql.sql_lookup import SQLDatabase, SQLiteQuery
from alexia.IGC_extractor import IGCWord, IGCExtractor
import csv

def lemma_output(IGC_folder, prop_names):
    """
    Iterates over the input corpus and returns the lemmas not found 
    in the DIM, ordered by frequency. Also includes information on 
    the number of nouns, indicating if a noun only exists in either
    the singular or the plural form (and whether the automatic 
    lemmatization/pos tagging is off). Can be altered for other 
    databases or corpora. 
    """
    dim = SQLDatabase(db_name='databases/dim_lemmas_word_forms.db')
    filters = SQLDatabase(db_name='databases/IGC_filters.db') # Predefined stop-word list based on the IGC
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    IGC = IGCExtractor(folder=str(IGC_folder))
    freqdic = {}

    print("""
    ============================================================
    Reading corpus files.
    ============================================================
    """)
    for word in IGC.extract(forms=False, lemmas=True, pos=True):
        try:
            if prop_names==False:
                if word.pos.startswith('n') and word.pos.endswith('s'): # Ignore proper names
                    continue
            if word.pos in pos_to_ignore:
                    continue
            if (not all(i.isalpha() or i == '-' for i in word.lemma)): # Ignore if not only letters or letters and hyphen
                continue
            if len(word.lemma) < 3: # Ignore very short words, likely to be particles
                continue
            if '-' in [word.lemma[0], word.lemma[1], word.lemma[-1]]: # Ignore words that start with '[anyLetter?]-' or end with '-'
                continue
            # Ignore unwanted words, such as names, foreign words, stopwords, abbreviations
            filter_query = SQLiteQuery(word.lemma,'filter','FILTER_WORD_FORMS', cursor=filters.cursor)
            if filter_query.exists:
                continue
            else:
                query = SQLiteQuery(word.lemma, 'lemma','DIM_ELEMENT', cursor = dim.cursor) # Capitalized words included
                query_lower = SQLiteQuery(word.lemma.lower(),'lemma','DIM_ELEMENT', cursor = dim.cursor)
                if not query.exists and not query_lower.exists: # If the word is not found in the DIM or the stopwords
                    if word.lemma in freqdic:
                        if word.pos[0] == 'n': # if word is a noun
                            freqdic[word.lemma]['freq'] += 1
                            if word.pos[2] == 'e': # if the noun is singular (eintala)
                                freqdic[word.lemma]['number']['sing'] += 1
                            elif word.pos[2] == 'f': # if the noun is plural (fleirtala)
                                freqdic[word.lemma]['number']['plur'] += 1                                
                        else:
                            freqdic[word.lemma]['freq'] += 1    # Necessary for proper names, nouns with no number
                            freqdic[word.lemma]['number']['no_number'] += 1
                    else:
                        if word.pos[0] == 'n':
                            if word.pos[2] == 'e':
                                freqdic[word.lemma] = {'freq': 0, 'number':
                                                        {'sing': 1, 'plur': 0, 'no_number': 0}}
                            elif word.pos[2] == 'f':
                                freqdic[word.lemma] = {'freq': 0, 'number':
                                                        {'sing': 0, 'plur': 1, 'no_number': 0}}
                            else:
                                freqdic[word.lemma] = {'freq': 0, 'number':
                                                    {'sing': 0, 'plur': 0, 'no_number': 1}} 
                        else:
                            freqdic[word.lemma] = {'freq': 0, 'number':
                                                    {'sing': 0, 'plur': 0, 'no_number': 1}} 
                        freqdic[word.lemma]['freq'] = 1                           
        except IndexError:
            continue
        except ET.ParseError:
            continue
    
    print("""
    ============================================================
    Sorting candidate frequencies.
    ============================================================
    """)

    if IGC_folder == "corpora/IGC/":
        with open('output/DIM/IGC_lemma.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file IGC_lemma.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)                
    elif IGC_folder == "corpora/IGC/CC_BY/":
        with open('output/DIM/CC_BY_lemma.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file CC_BY_lemma.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)
    elif IGC_folder == "corpora/IGC/TIC/":
        with open('output/DIM/TIC_lemma.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file TIC_lemma.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)    
    else:
        namefolder = IGC_folder.split("/")[3]
        with open('output/DIM/'+namefolder+'_lemma.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')

        print(f"""
    ============================================================
    Output file {namefolder}_lemma.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)

def wordform_output(IGC_folder, prop_names):
    """
    Iterates over the input corpus and returns the word forms not found 
    in the DIM, ordered by frequency. Can be altered for other 
    databases or corpora. 
    """
    dim = SQLDatabase(db_name='databases/dim_lemmas_word_forms.db')
    filters = SQLDatabase(db_name='databases/IGC_filters.db') # Predefined stop-word list based on the IGC
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    IGC = IGCExtractor(folder=str(IGC_folder))
    freqdic = {}
    print("""
    ============================================================
    Reading corpus files.
    ============================================================
    """)
    for word in IGC.extract(forms=True, lemmas=False, pos=True):
        try:
            if prop_names==False:
                if word.pos.startswith('n') and word.pos.endswith('s'): # Ignore proper names
                    continue
            if word.pos in pos_to_ignore:
                    continue
            if (not all(i.isalpha() or i == '-' for i in word.word_form)): # Ignore if not only letters or letters and hyphen
                continue
            if len(word.word_form) < 3:
                continue
            if '-' in [word.word_form[0], word.word_form[1], word.word_form[-1]]: # Ignore words that start with '[anyLetter?]-' or end with '-'
                continue
            # Ignore unwanted words, such as names, foreign words, stopwords, abbreviations
            filter_query = SQLiteQuery(word.word_form,'filter','FILTER_WORD_FORMS', cursor=filters.cursor)
            if filter_query.exists:
                continue
            else:
                query = SQLiteQuery(word.word_form, 'word_form','DIM_ELEMENT', cursor = dim.cursor) # Capitalized words included
                query_lower = SQLiteQuery(word.word_form.lower(),'word_form','DIM_ELEMENT', cursor = dim.cursor)
                if not query.exists and not query_lower.exists: # If the word is not found in the DIM or the stopwords
                    if word.word_form in freqdic:
                        freqdic[word.word_form] += 1
                    else:
                        freqdic[word.word_form] = 1              
        except IndexError:
            continue
        except ET.ParseError:
            continue
    print("""
    ============================================================
    Sorting candidate frequencies.
    ============================================================
    """)
    
    if IGC_folder == "corpora/IGC/":
        with open('output/DIM/IGC_wordform.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file IGC_wordforms.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)                
    elif IGC_folder == "corpora/IGC/CC_BY/":
        with open('output/DIM/CC_BY_wordform.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file CC_BY_wordforms.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)

    elif IGC_folder == "corpora/IGC/TIC/":
        with open('output/DIM/TIC_wordform.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file TIC_wordforms.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)

    else:
        namefolder = IGC_folder.split("/")[3]
        with open('output/DIM/'+namefolder+'_wordform.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')

        print(f"""
    ============================================================
    Output file {namefolder}_wordforms.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)