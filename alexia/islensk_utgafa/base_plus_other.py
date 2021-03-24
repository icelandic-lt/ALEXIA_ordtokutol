from xml.etree import ElementTree as ET
from string import punctuation
import glob
from alexia.sql.sql_lookup import SQLDatabase, SQLiteQuery
from alexia.IGC_extractor import IGCWord, IGCExtractor

def lemmabase_wordforms(database, IGC_folder, prop_names):
    """
    Iterates through the IGC, outputting a list of lemmas
    and their frequencies as well as all wordforms that appear
    alongside the lemma in the corpus. Useful for detecting whether
    a word only appears in certain context (e.g. fixed expressions)
    or whether a certain wordform never appears. Can be modified to 
    fit the user's need.
    """
    dci = SQLDatabase(db_name='gagnagrunnar/nmo.db')
    dim = SQLDatabase(db_name='gagnagrunnar/bin_lemmur_ordmyndir.db')
    filters = SQLDatabase(db_name='gagnagrunnar/IGC_filters.db') # Predefined stop-word list based on the RMH
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    IGC = IGCExtractor(folder=str(IGC_folder))
    freqdic = {}
    
    print("""
    ============================================================
    Les skjöl úr málheildinni.
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
                if database == 'NMO':
                    query = SQLiteQuery(word.lemma, 'lemma','DCI_ELEMENT', cursor = dci.cursor) # Capitalized words included
                    query_lower = SQLiteQuery(word.lemma.lower(),'lemma','DCI_ELEMENT', cursor = dci.cursor)
                elif database == 'BIN':
                    query = SQLiteQuery(word.lemma, 'lemma','DIM_ELEMENT', cursor = dim.cursor) # Capitalized words included
                    query_lower = SQLiteQuery(word.lemma.lower(),'lemma','DIM_ELEMENT', cursor = dim.cursor)
                if not query.exists and not query_lower.exists:
                    if word.lemma in freqdic:
                        if word.word_form not in freqdic[word.lemma]['orðmyndir']:
                            freqdic[word.lemma]['orðmyndir'].append(word.word_form)
                        freqdic[word.lemma]['tíðni'] += 1
                    else:
                        freqdic[word.lemma] = {}
                        freqdic[word.lemma]['tíðni'] = 1
                        freqdic[word.lemma]['orðmyndir'] = [word.word_form]
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
        with open(f'uttak/{database}/RMH_lemmur_med_ordmyndum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið RMH_lemmur_med_ordmyndum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/{database}/
    ============================================================
        """)                
    elif IGC_folder == "malheildir/RMH/CC_BY/":
        with open(f'uttak/{database}/CC_BY_lemmur_med_ordmyndum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið CC_BY_lemmur_med_ordmyndum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/{database}/
    ============================================================
        """)
    elif IGC_folder == "malheildir/RMH/MIM/":
        with open(f'uttak/{database}/MIM_lemmur_med_ordmyndum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið MIM_lemmur_med_ordmyndum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/{database}/    
    ============================================================
        """)    
    else:
        namefolder = IGC_folder.split("/")[3]
        with open(f'uttak/{database}/'+namefolder+'_lemmur_med_ordmyndum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')

        print(f"""
    ============================================================
    Úttaksskjalið {database}_lemmur_med_ordmyndum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/{database}/
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
    dim = SQLDatabase(db_name='gagnagrunnar/bin_lemmur_ordmyndir.db')
    filters = SQLDatabase(db_name='gagnagrunnar/IGC_filters.db') # Predefined stop-word list based on the RMH
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    IGC = IGCExtractor(folder=str(IGC_folder))
    freqdic = {}
    
    print("""
    ============================================================
    Les skjöl úr málheildinni.
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
                        if word.lemma not in freqdic[word.word_form]['lemmur']:
                            freqdic[word.word_form]['lemmur'].append(word.lemma)
                        freqdic[word.word_form]['tíðni'] += 1
                    else:
                        freqdic[word.word_form] = {}
                        freqdic[word.word_form]['tíðni'] = 1
                        freqdic[word.word_form]['lemmur'] = [word.lemma]
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
        with open('uttak/BIN/RMH_ordmyndir_med_lemmum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið RMH_ordmyndir_med_lemmum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/BIN/   
    ============================================================
        """)                
    elif IGC_folder == "malheildir/RMH/CC_BY/":
        with open('uttak/BIN/CC_BY_ordmyndir_med_lemmum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið CC_BY_ordmyndir_med_lemmum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/BIN/
    ============================================================
        """)
    elif IGC_folder == "malheildir/RMH/MIM/":
        with open('uttak/BIN/MIM_ordmyndir_med_lemmum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið MIM_ordmyndir_med_lemmum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/BIN/    
    ============================================================
        """)    
    else:
        namefolder = IGC_folder.split("/")[3]
        with open('uttak/BIN/'+namefolder+'_ordmyndir_med_lemmum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(freqdic.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)}
            for key, value in candidates.items():
                outputfile.write(key+': '+str(value)+ '\n')
        print(f"""
    ============================================================
    Úttaksskjalið {namefolder}_ordmyndir_med_lemmum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/BIN/
    ============================================================
        """)