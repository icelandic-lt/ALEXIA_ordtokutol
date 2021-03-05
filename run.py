"""
This script leads the user through a series of questions that define
the format of the output. The initial settings ask the user to choose
between the demo version and a user-defined input version of the 
program. 
"""

import sys
from pathlib import Path
from alexia.find_texttype_freqs import texttype_freqs
from alexia.txt_to_data import user_defined_freqlist
from alexia.base_output import lemma_output, wordform_output
from alexia.base_plus_other import lemmabase_wordforms, wordformbase_lemmas
from alexia.collocation_output import user_defined_collocations

# INITIAL SETTINGS

def greeting():
    print("""
    ============================================================
    Welcome to ALEXIA, the lexicon acquisition tool. Please
    make sure you have completed the necessary database creation
    in the setup.py file included in the package. 
    Do you want to choose your own input or proceed to 
    the demo version?
    ============================================================
    """)
    default_or_user_defined()

def default_or_user_defined():
    print("""
    ============================================================
    Enter the number corresponding to your choice and press ENTER.
    ============================================================
    """)

    initial_choice = input("""
    (1) Own input
    (2) Demo version
        """)
    if initial_choice == "1":
        user_defined()

    elif initial_choice == "2":
        default()
    else:
        print("""
    ============================================================
    This is not a valid option, please try again.
    ============================================================
        """)
        initial_choice = default_or_user_defined()

# USER-DEFINED CHOICES

def enter_file():
    filename = input("""
    Enter the file path:
    """)
    if filename == 'None':
        print(f"""
    ============================================================
    No file chosen.
    ============================================================
        """)
    elif not Path(filename).is_file():
        print(f"""
    ============================================================
    The file {filename} does not exist. Please try again.
    ============================================================
        """)
        filename = enter_file()
    else:
        pass 
    return filename

def enter_directory():
    directory = input("""
    Please enter the full directory path:
    """)
    if not Path(directory).is_dir():
        print(f"""
    ============================================================
    The directory {directory} does not exist. Please try again.
    ============================================================
        """)
        directory = enter_directory()
    else:
        print(f"""
    ============================================================
    {directory} chosen.
    ============================================================
        """)
    return directory

def enter_output():
    output = number_input(2)
    if output == '1':
        print(f"""
    ============================================================
    Frequency list chosen.
    ============================================================
        """)
    elif output == '2':
        print(f"""
    ============================================================
    Collocation list chosen.
    ============================================================
        """)    
    return output

def user_defined():
    print("""
    ============================================================
    You have chosen to enter your own input.
    ============================================================
    Please provide the full file path for your database, 
    ending in .db

    Example: databases/lexicon.db
    ============================================================
    """)
    database = enter_file()
    if database == 'None':
        print("""
    ============================================================
    You cannot proceed with no input database. 
    ============================================================
        """)
        sys.exit(1)
    else:
        print(f"""
    ============================================================
    Your input database is: {database}
    ============================================================
    Please provide the full directory path for the corpus to be 
    used for comparison. Note that the program assumes that the 
    corpus is in plain txt-format.

    Example: corpora/txtcorpus
    ============================================================
        """)
    corpus = enter_directory()
    print(f"""
    ============================================================
    Your comparison corpus is: {corpus}
    ============================================================
    Please indicate whether or not you want to use a stopword 
    filter database. 

    To use a database, please provide the full file path. 
    To skip this step, please write 'None'
    ============================================================
    """)
    filters = enter_file()
    if filters == 'None':
        print(f"""
    ============================================================
    No filters chosen. 
    ============================================================
        """)
    else:
        print(f"""
    ============================================================
    {filters} chosen as filter database. 
    ============================================================
        """)
    
    print("""
    ============================================================
    Choose your output.
    ============================================================
    1 Frequency word list (word, frequency)
    2 Frequency word list including collocation examples on each
    candidate (word: freq. [sent example 1, sent example 2...])

    Enter the number corresponding to your choice and press ENTER.
    ============================================================
        """)

    output = enter_output()
    if output == '1':
        user_defined_freqlist(database, filters, corpus)
    elif output == '2':
        user_defined_collocations(database,filters,corpus)

# DEMO VERSION CHOICES

def number_input(limit):
    number = input("""
        Enter number:
    """)
    try:
        if int(number) > int(limit) or int(number) == 0:
            print(f"""
    ============================================================
    {number} is not a valid option. Please try again.
    ============================================================
            """)
            number = number_input(limit)
    except ValueError:
        print(f"""
    ============================================================
    You must enter a number. Please try again.
    ============================================================
        """)
        number = number_input(limit)

    return number

def prop_names():
    print("""
    ============================================================
    Please indicate if you want to exclude
    proper names from the results.
    
    This can be beneficial as proper names tend to overflood
    the candidate lists. 

    1 Exclude proper names
    2 Include proper names
    ============================================================
        """)
    prop_names = number_input(2)
    if prop_names == '1':
        print("""
    ============================================================
    Proper names excluded.
    ============================================================
        """)
    elif prop_names == '2':
        print("""
    ============================================================
    Proper names included.
    ============================================================
        """)
    return prop_names

def lemmas_or_wordforms():
    print("""
    ============================================================
    Please indicate whether you want to use lemmas or 
    word forms as the base for your output candidate list. 

    1 Lemmas
    2 Word forms
    ============================================================
    """)
    base_form = number_input(2)
    if base_form == '1':
        print("""
    ============================================================
    Lemmas chosen.
    ============================================================
        """)
    elif base_form == '2':
        print("""
    ============================================================
    Word forms chosen.
    ============================================================
        """)
    return base_form

def default_output(base_form):
    if base_form == '1': # lemmas
        print("""
    ============================================================
    Please choose a type of output candidate list.
    Enter the number corresponding to your choice and press ENTER. 

    1 Frequency list (lemma, freq) including information on whether
    a noun appears more frequently in the singular or plural.
        
    2 Frequency list including all word forms appearing with 
    the lemma (lemma, freq [word form])

    3 Frequency list including individual frequencies from various 
    text types (lemma, total freq: maths, freq, news, freq...)
    ============================================================
        """)
        choice = number_input(3)
    elif base_form == '2': # word forms
        print("""
    ============================================================
    Please choose a type of output candidate list.
    Enter the number corresponding to your choice and press ENTER. 

    1 Frequency list (word form, freq)
        
    2 Frequency list including all lemmas appearing with 
    the word form (word form, freq [lemma])
    ============================================================
        """)
        choice = number_input(2)
    return choice
    

def default():
    print("""
    ============================================================
    This is the demo version of ALEXIA. 

    By default, the input lexicon is the Database of Icelandic
    Morphology (DIM) and the comparison corpus is the Icelandic
    Gigaword Corpus (IGC). 
        
    Please make sure that you have completed the necessary 
    database creation in setup.py and that the IGC is stored 
    as the example directories indicate, that is to say, in 
    the path ./corpora/IGC/ and with the subdirectories 
    CC_BY and MIM.  
    ============================================================
    Please indicate which part of the IGC you want to use for
    comparison.
        
    1 Entire corpus
    2 CC_BY (the open-source half of the IGC)
    3 TIC (Tagged Icelandic Corpus, the liecensed half of the IGC)
    4 Specific subdirectory (within either subcorpora)
    ============================================================
    """)
    
    corpus_part = number_input(4)
    if corpus_part == "1":
        if not Path('corpora/IGC/').is_dir():
            print(f"""
    ============================================================
    The directory corpora/IGC/ does not exist. Please make sure 
    that the IGC is stored in the same way as the example
    directories.
    ============================================================
        """)     
        else:
            print(f"""
    ============================================================
    Entire IGC chosen. 
    ============================================================
            """)
            propnames = prop_names()
            base_form = lemmas_or_wordforms()
            output = default_output(base_form)

            if base_form == '1': # Lemmas
                if propnames == '1': # excluded
                    if output == '1': # plain freq list
                        lemma_output("corpora/IGC/", prop_names=False) 
                    elif output == '2': # lemma freqs + all word forms
                        lemmabase_wordforms("corpora/IGC/", prop_names=False) 
                    elif output == '3': # lemma freqs + text types
                        texttype_freqs("corpora/IGC/", prop_names=False) 

                elif propnames == '2': # included
                    if output == '1':
                        lemma_output("corpora/IGC/", prop_names=True)
                    elif output == '2': 
                        lemmabase_wordforms("corpora/IGC/", prop_names=True)
                    elif output == '3': 
                        texttype_freqs("corpora/IGC/", prop_names=True)

            elif base_form == '2': # Word forms
                if propnames == '1':
                    if output == '1':
                        wordform_output("corpora/IGC/", prop_names=False)
                    elif output == '2':
                        wordformbase_lemmas("corpora/IGC/", prop_names=False)
                elif propnames == '2':
                    if output == '1':
                        wordform_output("corpora/IGC/", prop_names=True)
                    elif output == '2':
                        wordformbase_lemmas("corpora/IGC/", prop_names=True)
    elif corpus_part == "2":
        if not Path('corpora/IGC/CC_BY').is_dir():
            print(f"""
    ============================================================
    The directory corpora/IGC/CC_BY does not exist. Please make 
    sure that the IGC is stored in the same way as the example
    directories.        
    ============================================================
    """)             
        else:
            print(f"""
    ============================================================
    CC_BY chosen. 
    ============================================================
            """)
            propnames = prop_names()
            base_form = lemmas_or_wordforms()
            output = default_output(base_form)
            if base_form == '1': # Lemmas        
                if propnames == '1': 
                    if output == '1': 
                        lemma_output("corpora/IGC/CC_BY/", prop_names=False)
                    elif output == '2': 
                        lemmabase_wordforms("corpora/IGC/CC_BY/", prop_names=False)
                    elif output == '3': 
                        texttype_freqs("corpora/IGC/CC_BY/", prop_names=False)

                elif propnames == '2': 
                    if output == '1':
                        lemma_output("corpora/IGC/CC_BY/", prop_names=True)
                    elif output == '2': 
                        lemmabase_wordforms("corpora/IGC/CC_BY/", prop_names=True)
                    elif output == '3': 
                        texttype_freqs("corpora/IGC/CC_BY/", prop_names=True)

            elif base_form == '2': # Word forms
                if propnames == '1':
                    if output == '1':
                        wordform_output("corpora/IGC/CC_BY/", prop_names=False)
                    elif output == '2':
                        wordformbase_lemmas("corpora/IGC/CC_BY/", prop_names=False)
                elif propnames == '2':
                    if output == '1':
                        wordform_output("corpora/IGC/CC_BY/", prop_names=True)
                    elif output == '2':
                        wordformbase_lemmas("corpora/IGC/CC_BY/", prop_names=True)            
    elif corpus_part == "3":
        if not Path('corpora/IGC/CC_BY').is_dir():
            print(f"""
    ============================================================
    The directory corpora/IGC/TIC does not exist. Please make 
    sure that the IGC is stored in the same way as the example
    directories.        
    ============================================================
            """)             
        else:        
            print(f"""
    ============================================================
    TIC chosen. 
    ============================================================
            """)
            propnames = prop_names()
            base_form = lemmas_or_wordforms()
            output = default_output(base_form)
            if base_form == '1': # Lemmas
                if propnames == '1': 
                    if output == '1': 
                        lemma_output("corpora/IGC/TIC/", prop_names=False)
                    elif output == '2': 
                        lemmabase_wordforms("corpora/IGC/TIC/", prop_names=False)
                    elif output == '3': 
                        texttype_freqs("corpora/IGC/TIC/", prop_names=False)

                elif propnames == '2': 
                    if output == '1':
                        lemma_output("corpora/IGC/TIC/", prop_names=True)
                    elif output == '2': 
                        lemmabase_wordforms("corpora/IGC/TIC/", prop_names=True)
                    elif output == '3': 
                        texttype_freqs("corpora/IGC/TIC/", prop_names=True)

            elif base_form == '2': # Word forms
                if propnames == '1':
                    if output == '1':
                        wordform_output("corpora/IGC/TIC/", prop_names=False)
                    elif output == '2':
                        wordformbase_lemmas("corpora/IGC/TIC/", prop_names=False)
                elif propnames == '2':
                    if output == '1':
                        wordform_output("corpora/IGC/TIC/", prop_names=True)
                    elif output == '2':
                        wordformbase_lemmas("corpora/IGC/TIC/", prop_names=True)

    elif corpus_part == "4":
        print(f"""
    ============================================================
    Specific subdirectory chosen. Please provide the full path
    to the subdirectory.

    Example: corpora/IGC/CC_BY/subdirectory
    ============================================================
            """)
        subdir = enter_directory()
        propnames = prop_names()
        base_form = lemmas_or_wordforms()
        output = default_output(base_form)
        if base_form == '1': # Lemmas
            if propnames == '1': 
                if output == '1': 
                    lemma_output(subdir, prop_names=False)
                elif output == '2': 
                    lemmabase_wordforms(subdir, prop_names=False)
                elif output == '3': 
                    texttype_freqs(subdir, prop_names=False)
            elif propnames == '2': 
                if output == '1':
                    lemma_output(subdir, prop_names=True)
                elif output == '2': 
                    lemmabase_wordforms(subdir, prop_names=True)
                elif output == '3': 
                    texttype_freqs(subdir, prop_names=True)
        elif base_form == '2': # Word forms
            if propnames == '1':
                if output == '1':
                    wordform_output(subdir, prop_names=False)
                elif output == '2':
                    wordformbase_lemmas(subdir, prop_names=False)
            elif propnames == '2':
                if output == '1':
                    wordform_output(subdir, prop_names=True)
                elif output == '2':
                    wordformbase_lemmas(subdir, prop_names=False)

# MAIN
greeting()