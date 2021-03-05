from string import punctuation
import xml.etree.ElementTree as ET
import glob
import csv
from alexia.sql.sql_lookup import SQLDatabase, SQLiteQuery
from progress.bar import IncrementalBar
import sys


def texttype_freqs(folder, prop_names):
    """
    Used to collect lemmas by the types of text they appear in and sort
    them by frequency. Filters the IGC in order to retrieve the desired
    results. The script can be modified according to the user's need 
    and to fit another corpus.  
    """
    dim = SQLDatabase(db_name='databases/dim_lemmas_word_forms.db')
    filters = SQLDatabase(db_name='databases/IGC_filters.db') # Predefined stop-word list based on the IGC

    print("""
    ============================================================
    Reading corpus files.
    ============================================================
    """)
    xml_files = glob.glob(folder+'/**/*.xml', recursive=True)

    alltexttypes = []
    freqdic1 = {}
    freqdic2 = {}
    filebar = IncrementalBar('Progress', max = len(xml_files))
    for file in xml_files:
        with open(file, 'r', encoding='utf-8') as content:
            try:
                tree = ET.parse(content)
                root = tree.getroot()
                textClass = root[0][2][0][0][0][0] # Retrieve the texttype tag from the XML file
                texttype = textClass.text 
                if texttype not in alltexttypes:
                    alltexttypes.append(texttype) # Collect all unique texttypes
                pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au'] # The POS tags that should not be displayed in the results
                for word in tree.iter():
                    pos = word.attrib.get('type')
                    if pos is not None:
                        if prop_names==False:
                            if pos.startswith('n') and pos.endswith('s'): # Ignore proper names
                                continue
                        if pos in pos_to_ignore:
                            continue
                        if (not all(i.isalpha() or i == '-' for i in word.text)): # Ignore all that are not alphabetic letters or hyphen 
                            continue
                        if len(word.text) < 3: # Ignore very short words, likely to be particles
                            continue
                        if word.text[-1] == '-': # Ignore words starting or ending with a hypen (likely OCR errors)
                            continue
                        if word.text[0] == '-':
                            continue
                        if word.attrib.get('lemma') is not None:
                            lemma = word.attrib.get('lemma')
                            filter_query = SQLiteQuery(lemma,'filter','FILTER_WORD_FORMS', cursor=filters.cursor) # Ignore stop words
                            if filter_query.exists:
                                continue
                            else:
                                query = SQLiteQuery(lemma,'lemma','DIM_ELEMENT', cursor = dim.cursor) # Capitalized words included
                                query_lower = SQLiteQuery(lemma.lower(),'lemma','DIM_ELEMENT', cursor = dim.cursor) # Only lowercase
                                if not query.exists and not query_lower.exists: # If the word is not found in the DIM or the stopwords
                                    if lemma not in freqdic1: # Collect total freqs
                                        freqdic1[lemma] = 1
                                    else:
                                        freqdic1[lemma] += 1
                                    if (lemma,texttype) not in freqdic2: # Collect texttype freqs
                                        freqdic2[(lemma,texttype)] = 1
                                    else:
                                        freqdic2[(lemma,texttype)] += 1
            except IndexError:
                continue
            except ET.ParseError:
                continue

        filebar.next()
        sys.stdout.flush()
    filebar.finish()

    print("""
    ============================================================
    Sorting frequencies by text types. 
    ============================================================
    """)

    tempfinal = []
    bar1 = IncrementalBar('Progress', max = len(freqdic1))
    for key, value in sorted(freqdic1.items()): # Lemma, total freq
        tempf = []
        tempf.append(key)
        temp = []
        for k, v in freqdic2.items(): 
            if k[0] == key:
                temp.append((k[1], v)) # A list of all possible texttypes that appear with the lemma
        for tt in alltexttypes:
            if tt in [item[0] for item in temp]:
                continue
            else:
                temp.append((tt, 0)) 
        tempf.append(value)
        for tup in sorted(temp):
            tempf.append(tup[1]) 
        tempfinal.append(tempf) # The format of this list is [lemma, totalfreq, texttype_a freq, texttype_b freq...]
        bar1.next()
        sys.stdout.flush()
    bar1.finish()

    header = ['Word', 'Total freq'] + sorted(alltexttypes)

    if folder == "corpora/IGC/":
        with open("output/DIM/IGC_texttypes.csv", mode='w+') as outputfile:
            csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(header)
            for i in tempfinal:
                csvwriter.writerow(i)
        print("""
    ============================================================
    Output file IGC_texttypes.csv is ready and can be found
    in the output/DIM/ directory.
    ============================================================
        """)
    elif folder == "corpora/IGC/CC_BY/":
        with open('output/DIM/CC_BY_texttypes.csv', mode='w+') as outputfile:
            csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(header)
            for i in tempfinal:
                csvwriter.writerow(i)
        print("""
    ============================================================
    Output file CC_BY_texttypes.csv is ready and can be found
    in the output/DIM/ directory.
    ============================================================
        """)
    elif folder == "corpora/IGC/TIC/":
        with open('output/DIM/TIC_texttypes.csv', mode='w+') as outputfile:
            csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(header)
            for i in tempfinal:
                csvwriter.writerow(i)
        print("""
    ============================================================
    Output file TIC_texttypes.csv is ready and can be found
    in the output/DIM/ directory.
    ============================================================
        """)
    else:
        namefolder = folder.split("/")[3]
        with open('output/DIM/'+namefolder+"_texttypes.csv", mode='w+') as outputfile:
           csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           csvwriter.writerow(header)
           for i in tempfinal:
               csvwriter.writerow(i)

        print(f"""
    ============================================================
    Output file {namefolder}_texttypes.csv is ready and can be 
    found in the output/DIM/ directory.
    ============================================================
        """)


