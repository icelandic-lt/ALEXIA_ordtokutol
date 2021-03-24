from xml.etree import ElementTree as ET
from string import punctuation
import glob
from alexia.sql.sql_lookup import SQLDatabase, SQLiteQuery
from alexia.IGC_extractor import IGCWord, IGCExtractor
import csv

def lemma_output(database, IGC_folder, prop_names):
    """
    Iterates over the input corpus and returns the lemmas not found 
    in the input database, ordered by frequency. Also includes 
    information on the tala of nouns, indicating if a noun only 
    exists in either the singular or the plural form (and whether 
    the automatic lemmatization/pos tagging is off). Can be altered 
    for other databases or malheildir. 
    """
    dci = SQLDatabase(db_name='gagnagrunnar/nmo.db')
    dim = SQLDatabase(db_name='gagnagrunnar/bin_lemmur_ordmyndir.db')
    filters = SQLDatabase(db_name='gagnagrunnar/IGC_filters.db') # Predefined stop-word list based on the RMH
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    RMH = IGCExtractor(folder=str(IGC_folder))
    freqdic = {}

    print("""
    ============================================================
    Les skjöl úr málheildinni.
    ============================================================
    """)
    for word in RMH.extract(forms=False, lemmas=True, pos=True):
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
                if database == 'NMO':
                    query = SQLiteQuery(word.lemma, 'lemma','DCI_ELEMENT', cursor = dci.cursor) # Capitalized words included
                    query_lower = SQLiteQuery(word.lemma.lower(),'lemma','DCI_ELEMENT', cursor = dci.cursor)
                elif database == 'BIN':
                    query = SQLiteQuery(word.lemma, 'lemma','DIM_ELEMENT', cursor = dim.cursor) # Capitalized words included
                    query_lower = SQLiteQuery(word.lemma.lower(),'lemma','DIM_ELEMENT', cursor = dim.cursor)
                
                if not query.exists and not query_lower.exists: # If the word is not found in the BIN or the stopwords
                    if word.lemma in freqdic:
                        if word.pos[0] == 'n': # if word is a noun
                            freqdic[word.lemma]['tíðni'] += 1
                            if word.pos[2] == 'e': # if the noun is singular (eintala)
                                freqdic[word.lemma]['tala']['eintala'] += 1
                            elif word.pos[2] == 'f': # if the noun is plural (fleirtala)
                                freqdic[word.lemma]['tala']['fleirtala'] += 1                                
                        else:
                            freqdic[word.lemma]['tíðni'] += 1    # Necessary for proper names, nouns with no tala
                            freqdic[word.lemma]['tala']['engin_tala'] += 1
                    else:
                        if word.pos[0] == 'n':
                            if word.pos[2] == 'e':
                                freqdic[word.lemma] = {'tíðni': 0, 'tala':
                                                        {'eintala': 1, 'fleirtala': 0, 'engin_tala': 0}}
                            elif word.pos[2] == 'f':
                                freqdic[word.lemma] = {'tíðni': 0, 'tala':
                                                        {'eintala': 0, 'fleirtala': 1, 'engin_tala': 0}}
                            else:
                                freqdic[word.lemma] = {'tíðni': 0, 'tala':
                                                    {'eintala': 0, 'fleirtala': 0, 'engin_tala': 1}} 
                        else:
                            freqdic[word.lemma] = {'tíðni': 0, 'tala':
                                                    {'eintala': 0, 'fleirtala': 0, 'engin_tala': 1}} 
                        freqdic[word.lemma]['tíðni'] = 1                           
        except IndexError:
            continue
        except ET.ParseError:
            continue
    
    print("""
    ============================================================
    Flokkar orð eftir tíðni.
    ============================================================
    """)
    if IGC_folder == "malheildir/RMH/":
        with open(f'uttak/{database}/RMH_lemmur.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið RMH_lemmur.freq er tilbúið og er að finna í 
    undirmöppunni uttak/{database}/
    ============================================================
        """)                
    elif IGC_folder == "malheildir/RMH/CC_BY/":
        with open(f'uttak/{database}/CC_BY_lemmur.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið CC_BY_lemmur.freq er tilbúið og er að finna í 
    undirmöppunni uttak/{database}/    
    ============================================================
        """)
    elif IGC_folder == "malheildir/RMH/MIM/":
        with open(f'uttak/{database}/MIM_lemmur.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið MIM_lemmur.freq er tilbúið og er að finna í 
    undirmöppunni uttak/{database}/    
    ============================================================
        """)    
    else:
        namefolder = IGC_folder.split("/")[3]
        with open(f'uttak/{database}/'+namefolder+'_lemmur.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')

        print(f"""
    ============================================================
    Úttaksskjalið {namefolder}_lemmur.freq er tilbúið og er að finna í 
    undirmöppunni uttak/{database}/    
    ============================================================
        """)

def wordform_output(IGC_folder, prop_names):
    """
    Iterates over the input corpus and returns the word forms not found 
    in the BIN, ordered by frequency. Can be altered for other 
    gagnagrunnar or malheildir. 
    """
    dim = SQLDatabase(db_name='gagnagrunnar/bin_lemmur_ordmyndir.db')
    filters = SQLDatabase(db_name='gagnagrunnar/IGC_filters.db') # Predefined stop-word list based on the RMH
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    RMH = IGCExtractor(folder=str(IGC_folder))
    freqdic = {}
    print("""
    ============================================================
    Les skjöl úr málheildinni.
    ============================================================
    """)
    for word in RMH.extract(forms=True, lemmas=False, pos=True):
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
                if not query.exists and not query_lower.exists: # If the word is not found in the BIN or the stopwords
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
    Flokkar orð eftir tíðni.
    ============================================================
    """)
    
    if IGC_folder == "malheildir/RMH/":
        with open('uttak/BIN/RMH_ordmyndir.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Úttaksskjalið RMH_ordmyndir.freq er tilbúið og er að finna í 
    undirmöppunni uttak/BIN/
    ============================================================
        """)                
    elif IGC_folder == "malheildir/RMH/CC_BY/":
        with open('uttak/BIN/CC_BY_ordmyndir.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Úttaksskjalið CC_BY_ordmyndir.freq er tilbúið og er að finna í 
    undirmöppunni uttak/BIN/
    ============================================================
        """)

    elif IGC_folder == "malheildir/RMH/MIM/":
        with open('uttak/BIN/MIM_ordmyndir.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print("""
    ============================================================
    Úttaksskjalið MIM_ordmyndir.freq er tilbúið og er að finna í 
    undirmöppunni uttak/BIN/
    ============================================================
        """)

    else:
        namefolder = IGC_folder.split("/")[3]
        with open('uttak/BIN/'+namefolder+'_ordmyndir.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')

        print(f"""
    ============================================================
    Úttaksskjalið {namefolder}_ordmyndir.freq er tilbúið og er að finna í 
    undirmöppunni uttak/BIN/
    ============================================================
        """)