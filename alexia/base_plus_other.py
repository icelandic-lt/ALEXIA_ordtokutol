from xml.etree import ElementTree as ET
from string import punctuation
import glob
from alexia.sql.sql_lookup import SQLDatabase, SQLiteQuery
from alexia.IGC_extractor import IGCWord, IGCExtractor

def lemmabase_wordforms(IGC_folder, prop_names):
    """
    Iterates through the IGC, outputting a list of lemmas
    and their frequencies as well as all wordforms that appear
    alongside the lemma in the corpus. Useful for detecting whether
    a word only appears in certain context (e.g. fixed expressions)
    or whether a certain wordform never appears. Can be modified to 
    fit the user's need.
    """
    dim = SQLDatabase(db_name='databases/dim_lemmas_word_forms.db')
    filters = SQLDatabase(db_name='databases/filters.db') # Predefined stop-word list based on the IGC

    dim = SQLDatabase(db_name='databases/dim_lemmas_word_forms.db')
    filters = SQLDatabase(db_name='databases/filters.db') # Predefined stop-word list based on the IGC
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    IGC = IGCExtractor(folder=str(IGC_folder))
    freqdic = {}
    
    print("""
    ============================================================
    Reading corpus files.
    ============================================================
    """)

    for word in IGC.extract(forms=True, lemmas=True, pos=True):
        try:
            if prop_names==False:  
                if word.pos.startswith('n') and word.pos.endswith('s'):  # Ignore proper names
                    continue
            if word.pos in pos_to_ignore: 
                    continue
            if (not all(i.isalpha() or i == '-' for i in word.lemma)):  # Ignore if not only letters or letters and hyphen
                continue
            if len(word.lemma) < 3: # Ignore very short words, likely to be particles
                continue
            if '-' in [word.lemma[0], word.lemma[1], word.lemma[-1]]: # Ignore words that start with '[anyLetter?]-' or end with '-'
                continue
            # Ignore unwanted words, such as names, foreign words, stopwords, abbreviations
            filter_query = SQLiteQuery(word.lemma, 'filter', 'FILTER_WORD_FORMS', cursor=filters.cursor)
            if filter_query.exists:
                continue
            else:
                query = SQLiteQuery(word.lemma, 'lemma','DIM_ELEMENT', cursor = dim.cursor) # Capitalized words included
                query_lower = SQLiteQuery(word.lemma.lower(),'lemma','DIM_ELEMENT', cursor = dim.cursor)
                if not query.exists and not query_lower.exists:
                    if word.lemma in freqdic:
                        if word.word_form not in freqdic[word.lemma]['wordforms']:
                            freqdic[word.lemma]['wordforms'].append(word.word_form)
                        freqdic[word.lemma]['freq'] += 1
                    else:
                        freqdic[word.lemma] = {}
                        freqdic[word.lemma]['freq'] = 1
                        freqdic[word.lemma]['wordforms'] = [word.word_form]
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
        with open('output/DIM/IGC_lemma_plus_wordform.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file IGC_lemma_plus_wordform.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)                
    elif IGC_folder == "corpora/IGC/CC_BY/":
        with open('output/DIM/CC_BY_lemma_plus_wordform.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file CC_BY_lemma_plus_wordform.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)
    elif IGC_folder == "corpora/IGC/TIC/":
        with open('output/DIM/TIC_lemma_plus_wordform.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Output file TIC_lemma_plus_wordform.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)    
    else:
        namefolder = IGC_folder.split("/")[3]
        with open('output/DIM/'+namefolder+'_lemma_plus_wordform.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')

        print(f"""
    ============================================================
    Output file {namefolder}_lemma_plus_wordform.freq is ready 
    and can be found in the output/DIM/ directory.
    ============================================================
        """)

def wordformbase_lemmas(IGC_folder, prop_names):
    """
    Iterates through the IGC, outputting a list of wordforms
    and their frequencies as well as all lemmas that appear
    alongside the wordform in the corpus. Useful for detecting 
    if a wordform exists in multiple word classes and for 
    detecting errors in lemmatization. Can be modified to 
    fit the user's need.
    """
    dim = SQLDatabase(db_name='databases/dim_lemmas_word_forms.db')
    filters = SQLDatabase(db_name='databases/filters.db') # Predefined stop-word list based on the IGC

    dim = SQLDatabase(db_name='databases/dim_lemmas_word_forms.db')
    filters = SQLDatabase(db_name='databases/filters.db') # Predefined stop-word list based on the IGC
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    IGC = IGCExtractor(folder=str(IGC_folder))
    freqdic = {}
    
    print("""
    ============================================================
    Reading corpus files.
    ============================================================
    """)
    for word in IGC.extract(forms=True, lemmas=True, pos=True):
        try:
            if prop_names==False:  
                if word.pos.startswith('n') and word.pos.endswith('s'):  # Ignore proper names
                    continue
            if word.pos in pos_to_ignore: 
                    continue
            if (not all(i.isalpha() or i == '-' for i in word.word_form)):  # Ignore if not only letters or letters and hyphen
                continue
            if len(word.word_form) < 3: # Ignore very short words, likely to be particles
                continue
            if '-' in [word.word_form[0], word.word_form[1], word.word_form[-1]]: # Ignore words that start with '[anyLetter?]-' or end with '-'
                continue
            # Ignore unwanted words, such as names, foreign words, stopwords, abbreviations
            filter_query = SQLiteQuery(word.word_form, 'filter', 'FILTER_WORD_FORMS', cursor=filters.cursor)
            if filter_query.exists:
                continue
            else:
                query = SQLiteQuery(word.word_form, 'word_form','DIM_ELEMENT', cursor = dim.cursor) # Capitalized words included
                query_lower = SQLiteQuery(word.word_form.lower(),'word_form','DIM_ELEMENT', cursor = dim.cursor)
                if not query.exists and not query_lower.exists:
                    if word.word_form in freqdic:
                        if word.lemma not in freqdic[word.word_form]['lemmas']:
                            freqdic[word.word_form]['lemmas'].append(word.lemma)
                        freqdic[word.word_form]['freq'] += 1
                    else:
                        freqdic[word.word_form] = {}
                        freqdic[word.word_form]['freq'] = 1
                        freqdic[word.word_form]['lemmas'] = [word.lemma]
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
        with open('output/DIM/IGC_wordform_plus_lemma.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Output file IGC_wordform_plus_lemma.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)                
    elif IGC_folder == "corpora/IGC/CC_BY/":
        with open('output/DIM/CC_BY_wordform_plus_lemma.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Output file CC_BY_wordform_plus_lemma.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)
    elif IGC_folder == "corpora/IGC/TIC/":
        with open('output/DIM/TIC_wordform_plus_lemma.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Output file TIC_wordform_plus_lemma.freq is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)    
    else:
        namefolder = IGC_folder.split("/")[3]
        with open('output/DIM/'+namefolder+'_wordform_plus_lemma.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Output file {namefolder}_wordform_plus_lemma.freq is ready 
    and can be found in the output/DIM/ directory.
    ============================================================
        """)