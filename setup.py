"""
This script provides the user with a setup of the necessary
databases for ALEXIA. 
"""

import sys
from pathlib import Path
from alexia.prepare_data import prepare_data
from alexia.sql.corpus_to_sql import CorpusToSQL
from alexia.request_file import request_file

def greeting():
    current_python = sys.version_info[:2]
    required_python = (3, 6)

    if current_python < required_python:
        sys.stderr.write(f"""
    ============================================================
    Python version outdated.

    This software is dependent on Python {required_python[0]}.{required_python[1]}. but
    you are using Python {current_python[0]}.{current_python[1]}. Please update your
    version of Python. 
    ============================================================
    """)
        sys.exit(1)

    print("""
    ============================================================
    Welcome to the setup-process for ALEXIA. Please choose one
    of the following options by typing the corresponding number 
    and press ENTER.

    1 DEFAULT SET-UP: This process will create two databases
    automatically for you, the Database of Icelandic Morphology
    and a filter database based on a stop-word list compiled from
    the Icelandic Gigaword Corpus. Please make sure that the file
    IGC_filters.txt is stored at the top directory. If this option 
    is chosen, you do not have to enter any further information.

    2 USER SET-UP: After choosing this option, you will be asked 
    to enter the path to a txt-file containing a list of words, 
    similar to the example file lexicon.txt included in this 
    package. Please make sure that the file you enter includes 
    the header 'word', followed by a list of words, one word 
    per line. Optionally, you can also create a filter database 
    from a txt-file containing a list of tokens to be excluded
    from your results. 
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
    (1) Default set-up
    (2) User set-up
    """)

    if initial_choice == "1":
        default()

    elif initial_choice == "2":
        user_defined()
    else:
        print("""
    ============================================================
    This is not a valid option, please try again.
    ============================================================
    """)
        initial_choice = default_or_user_defined()

def enter_file():
    filename = input("""
    Enter the file path:
    """)
    if filename == 'N':
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

def name_database():
    db_name = input("""
    ============================================================
    Please enter a name for your database, not including the file
    ending .db

    Example: lexicon_database
    ============================================================
    """)

    if Path('databases/'+db_name+'.db').is_file():
        print(f"""
    ============================================================
    A database with the name {db_name}.db already exists. Please
    try again.
    ============================================================
        """)
        db_name = name_database()
    else:
        pass
    return db_name

def default():
    print("""
    ============================================================
    Default set-up initiated. Please wait while we set up the
    necessary databases.
    ============================================================
    """)
    sh_snid = 'SHsnid.csv'
    filters = 'IGC_filters.txt'

    if not Path('databases/filters.db').is_file():
        if Path(filters).is_file():
            print("""
    Preparing filters
            """)
            prepare_data(filters)
            print("""
    Creating filter database
            """)
            # Creates SQL database filters.db with header FILTER_WORD_FORMS
            filter_db = CorpusToSQL(corpus=filters, db_name='databases/IGC_filters')
            filter_db.create_db('FILTER_WORD_FORMS', 'filter')
        else:
            # Exit if IGC_filters.txt doesn't exist
            print(f"""
    The file <{filters}> does not exist. Aborting.
            """)
            sys.exit(1)
    else:
        print(f"""
    IGC filter database already exists.
        """)   

    if not Path('databases/dim_lemmas_word_forms.db').is_file():
        if not Path(sh_snid).is_file():
            print(f"""
    Downloading the required file <{sh_snid}> in order to set up DIM.
            """)
            request_file('https://bin.arnastofnun.is/django/api/nidurhal/?file=SHsnid.csv.zip',
                        'SHsnid.csv.zip', zipped=True)
        if Path(sh_snid).is_file():
            print("""
    Preparing DIM word forms and lemmas
            """)
            prepare_data(sh_snid)
            print("""
    Creating DIM word form and lemma database
                """)
            # Creates SQL database dim_lemmas_word_forms.db with header DIM_ELEMENT
            sh_snid = CorpusToSQL(corpus=sh_snid, db_name='databases/dim_lemmas_word_forms')
            sh_snid.create_relational_database('DIM_ELEMENT', 'lemma', 'word_form')
    else:
        print(f"""
    DIM database already exists.
        """)    
    
    print("""
    ============================================================
    Default set-up completed. The databases can be found in the
    subdirectory databases. Your next step is to run the file
    run.py from the command line.  
    ============================================================
    """)


def user_defined():
    print("""
    ============================================================
    Please enter the name of your lexicon file. This file should
    include a list of words that you wish to compare to an input
    corpus.

    Note that the path should be based on this directory. A file
    stored on the desktop might for example have the path: 
    ../../Desktop/lexicon.txt
    ============================================================
    """)

    db = enter_file()

    print("""
    Preparing data.
    """)

    prepare_data(db)
    db_name = name_database()

    print("""
    Creating database.
    """)

    # Creates SQL database (db_name).db, with header LEXICON_WORD
    lexicon = CorpusToSQL(corpus=db, db_name='databases/'+db_name)
    lexicon.create_db('LEXICON_WORD', 'word')

    print("""
    ============================================================
    If you wish to create a database of filters or stopwords to
    be excluded from your results, please enter a path to a file
    in txt-format, containing a list of words, one word per line,
    and a header 'filter'. 

    Note that the path should be based on this directory. A file
    stored on the desktop might for example have the path: 
    ../../Desktop/stopwords.txt

    If you do not wish to create such a database, please type
    'N' below and press ENTER. 
    ============================================================
    """)

    sw_db = enter_file()

    if sw_db == 'N':
        sys.exit(1)
    else:
        print("""
    Preparing stopword filters
        """)
        prepare_data(sw_db)
        
        sw_name = name_database()
        print("""
    Creating stopword filter database
        """)
        # Creates SQL database (sw_name).db with header FILTER_WORD_FORMS
        user_filter_db = CorpusToSQL(corpus=sw_db, db_name='databases/'+sw_name)
        user_filter_db.create_db('FILTER_WORD_FORMS', 'filter')
    
    print("""
    ============================================================
    User set-up completed. The databases can be found in the
    subdirectory databases. Your next step is to run the file
    run.py from the command line.  
    ============================================================
    """)

# MAIN
greeting()