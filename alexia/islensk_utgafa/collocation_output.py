import glob
import sqlite3
import xml.etree.ElementTree as ET
from string import punctuation
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
    if filterbase not in ['n', 'N']:
        filters = SQLDatabase(db_name=filterbase)
    else:
        pass    # if there is no filterbase, ignore this step

    outdict = {}
    
    print("""
    ============================================================
    Les skjöl úr málheildinni.
    ============================================================
    """)
    filebar = IncrementalBar('Framvinda', max = len(txt_files))
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
                if filterbase not in ['n', 'N']: # if a stopword database has been defined, filter the results
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
                                    if str(w1+' '+w2+' '+w+' '+w4+' '+w5) not in outdict[w]['orðstaða']:
                                        outdict[w]['orðstaða'][str(w1+' '+w2+' '+w+' '+w4+' '+w5)] = 1
                                    else:
                                        outdict[w]['orðstaða'][str(w1+' '+w2+' '+w+' '+w4+' '+w5)] += 1
                                    outdict[w]['tíðni'] += 1
                                else:
                                    outdict[w] = {}
                                    outdict[w]['tíðni'] = 1
                                    outdict[w]['orðstaða'] = {str(w1+' '+w2+' '+w+' '+w4+' '+w5): 1}

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
                                if str(w1+' '+w2+' '+w+' '+w4+' '+w5) not in outdict[w]['orðstaða']:
                                    outdict[w]['orðstaða'][str(w1+' '+w2+' '+w+' '+w4+' '+w5)] = 1
                                else:
                                    outdict[w]['orðstaða'][str(w1+' '+w2+' '+w+' '+w4+' '+w5)] += 1
                                outdict[w]['tíðni'] += 1
                            else:
                                outdict[w] = {}
                                outdict[w]['tíðni'] = 1
                                outdict[w]['orðstaða'] = {str(w1+' '+w2+' '+w+' '+w4+' '+w5): 1}
                        
        filebar.next()
        sys.stdout.flush()
    filebar.finish()


    output_file = input("""
    ============================================================
    Skrifaðu það sem þú vilt að úttaksskjalið heiti með 
    endingunni .freq
 
    Dæmi: ordasafn_ordstodulyklar.freq
    ============================================================
    """)

    with open('uttak/notendagogn/'+output_file, mode='w+') as outputfile:
        candidates = {k: v for k, v in sorted(outdict.items(),
                        key=lambda item: item[1]['tíðni'], reverse=True)} # Sort the candidates by their total frequencies
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
    Úttaksskjalið {output_file} er tilbúið og má finna í 
    undirmöppunni uttak/notendagogn/
    ============================================================
    """)


def lemmas_collocations(database, IGC_folder, prop_names):
    dci = SQLDatabase(db_name='gagnagrunnar/nmo.db')
    dim = SQLDatabase(db_name='gagnagrunnar/bin_lemmur_ordmyndir.db')
    filters = SQLDatabase(db_name='gagnagrunnar/IGC_filters.db') # Predefined stop-word list based on the RMH
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
    outdict = {}

    print("""
    ============================================================
    Les skjöl úr málheildinni. 
    ============================================================
    """)
    xml_files = glob.glob(IGC_folder+'/**/*.xml', recursive=True)

    filebar = IncrementalBar('Framvinda', max = len(xml_files))
    for file in xml_files:
        colloc = []
        with open(file, 'r', encoding='utf-8') as content:
            try:
                tree = ET.parse(content)
                for word in tree.iter():
                    if word.text is not None:
                        if word.attrib.get('lemma') is not None:
                            pos = word.attrib.get('type')
                            lemma = word.attrib.get('lemma')
                            word_form = word.text
                            colloc.append((word_form, lemma, pos))
                        elif word.text in punctuation:
                            colloc.append((word.text, ' ', ' '))

                for i, w in enumerate(colloc):
                    if prop_names==False:
                        if w[2].startswith('n') and w[2].endswith('s'): # Ignore proper names
                            continue
                    if w[2] in pos_to_ignore:
                        continue
                    if w[1][-1] == '-': # if a word starts or ends in an hyphen, ignore it (likely OCR error)
                        continue
                    if w[1][0] == '-':
                        continue
                    if (not all(i.isalpha() or i == '-' for i in w[1])): # if a word contains anything but an alphabetic letter or hyphen, ignore it
                        continue
                    filter_query = SQLiteQuery(w[1],'filter','FILTER_WORD_FORMS', cursor=filters.cursor) 
                    if filter_query.exists:
                        continue
                    else:
                        if database == 'NMO':
                            query = SQLiteQuery(w[1], 'lemma','DCI_ELEMENT', cursor = dci.cursor) # Capitalized words included
                            query_lower = SQLiteQuery(w[1].lower(),'lemma','DCI_ELEMENT', cursor = dci.cursor)
                        elif database == 'BIN':
                            query = SQLiteQuery(w[1], 'lemma','DIM_ELEMENT', cursor = dim.cursor) # Capitalized words included
                            query_lower = SQLiteQuery(w[1].lower(),'lemma','DIM_ELEMENT', cursor = dim.cursor)
                        if not query.exists and not query_lower.exists: # If the word is not found in the database nor the filters 
                            if len(w[1]) > 1: 
                                if i-2 < 0:     # collects 2 words before and after the candidate
                                    w1 = ""
                                else:
                                    w1 = str(colloc[i-2][0])
                                if i-1 < 0:
                                    w2 = ""
                                else:
                                    w2 = str(colloc[i-1][0])
                                if i+1 > len(colloc)-1: 
                                    w4 = ""
                                else:
                                    w4 = str(colloc[i+1][0])
                                if i+2 > len(colloc)-1:
                                    w5 = ""
                                else:
                                    w5 = str(colloc[i+2][0])
                                if w[1] in outdict:
                                    if str(w1+' '+w2+' '+w[0]+' '+w4+' '+w5) not in outdict[w[1]]['orðstaða']:
                                        outdict[w[1]]['orðstaða'][str(w1+' '+w2+' '+w[0]+' '+w4+' '+w5)] = 1
                                    else:
                                        outdict[w[1]]['orðstaða'][str(w1+' '+w2+' '+w[0]+' '+w4+' '+w5)] += 1
                                    outdict[w[1]]['tíðni'] += 1
                                else:
                                    outdict[w[1]] = {}
                                    outdict[w[1]]['tíðni'] = 1
                                    outdict[w[1]]['orðstaða'] = {str(w1+' '+w2+' '+w[0]+' '+w4+' '+w5): 1}
            except sqlite3.OperationalError:
                pass
        filebar.next()
        sys.stdout.flush()
    filebar.finish()

    if IGC_folder == "malheildir/RMH/":
        with open(f'uttak/{database}/RMH_lemmur_med_orstodulyklum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(outdict.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)} # Sort the candidates by their total frequencies
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
    Úttaksskjalið RMH_lemmur_med_orstodulyklum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/{database}/
    ============================================================
        """)

    elif IGC_folder == "malheildir/RMH/CC_BY/":
        with open(f'uttak/{database}/CC_BY_lemmur_med_orstodulyklum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(outdict.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)} # Sort the candidates by their total frequencies
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
    Úttaksskjalið CC_BY_lemmur_med_orstodulyklum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/{database}/
    ============================================================
        """)
    elif IGC_folder == "malheildir/RMH/MIM/":
        with open(f'uttak/{database}/MIM_lemmur_med_orstodulyklum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(outdict.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)} # Sort the candidates by their total frequencies
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
    Úttaksskjalið MIM_lemmur_med_orstodulyklum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/{database}/
    ============================================================
        """)    

    else:
        namefolder = IGC_folder.split("/")[3]
        with open(f'uttak/{database}/'+namefolder+'_lemmur_med_orstodulyklum.freq', mode='w+') as outputfile:
            candidates = {k: v for k, v in sorted(outdict.items(),
                            key=lambda item: item[1]['tíðni'], reverse=True)} # Sort the candidates by their total frequencies
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
    Úttaksskjalið {namefolder}_lemmur_med_orstodulyklum.freq er tilbúið og 
    er að finna í undirmöppunni uttak/{database}/
    ============================================================
        """)