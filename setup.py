"""
This script provides the user with a setup of the necessary
databases for ALEXIA. The script takes two command line arguments.

--input (or -i) is a filename to be used to create the lexicon database
defined by the user. The file should be stored in the top directory. 
This argument is required. However, if the user only wants to install 
the default options, the argument written should be --input default. 
If this option is chosen, the user does not have to define a list of 
stopwords as it is automatically generated. 

-- stopwords (or -sw) is a filename to be used to create a user-defined 
filter database, that is to say, a list of words that should be excluded
from the results. The file should be stored in the top directory. This 
argument is optional. 
"""

import sys
from pathlib import Path
from alexia.prepare_data import prepare_data
from alexia.sql.corpus_to_sql import CorpusToSQL
from alexia.request_file import request_file
import argparse
from argparse import SUPPRESS

current_python = sys.version_info[:2]
required_python = (3, 6)

if current_python < required_python:
    sys.stderr.write(f"""
    ==================================
    Python version outdated.
    ==================================
    This software is dependent on Python {required_python[0]}.{required_python[1]}. but
    you are using Python {current_python[0]}.{current_python[1]}. Please update your
    version of Python. 
""")
    sys.exit(1)

parser = argparse.ArgumentParser(description='ALEXIA lexicon acquisition tool.')
required = parser.add_argument_group('required arguments')

required.add_argument('-i','--input', 
    help='Please specify input file path or write "default". The input file should be a txt file stored in top dir, containing a header "word", followed by a list of words, one word per line', 
    required=True)
parser.add_argument('-sw','--stopwords', 
    help='Please specify path to txt containing stop-words. Should be a txt file stored in top dir, containing a header "filter", followed by a list of words, one word per line', 
    required=False)
args = parser.parse_args()

if args.input == "default":
    print("""
    ============================================================
    Default values selected. The default databases will be
    set up. Please make sure that IGC_filters.txt is stored
    at the top directory. 
    ============================================================
    """)

    sh_snid = 'SHsnid.csv'
    filters = 'IGC_filters.txt'

    if not Path('databases/filters.db').is_file():
        if Path(filters).is_file():
            print('Preparing filters')
            prepare_data(filters)
            print('Creating filter database')
            # Creates SQL database filters_ordmyndir.db with header FILTER_WORD_FORMS
            filter_db = CorpusToSQL(corpus=filters, db_name='databases/filters')
            filter_db.create_db('FILTER_WORD_FORMS', 'filter')
        else:
            # Exit if IGC_filters.txt doesn't exist
            print(f'The file <{filters}> does not exist. Aborting.')
            sys.exit(1)

    if not Path('databases/dim_lemmas_word_forms.db').is_file():
        if not Path(sh_snid).is_file():
            print(f'The required file <{sh_snid}> does not exist. Downloading file.')
            request_file('https://bin.arnastofnun.is/django/api/nidurhal/?file=SHsnid.csv.zip',
                        'SHsnid.csv.zip', zipped=True)
        if Path(sh_snid).is_file():
            print('Preparing DIM word forms and lemmas')
            prepare_data(sh_snid)
            print('Creating DIM word form and lemma database')
            # Creates SQL database dim_lemmas_word_forms.db with header DIM_ELEMENT
            sh_snid = CorpusToSQL(corpus=sh_snid, db_name='databases/dim_lemmas_word_forms')
            sh_snid.create_relational_database('DIM_ELEMENT', 'lemma', 'word_form')
    else:
        print(f'DIM database already exists.')    

elif not Path(args.input).is_file():
    print("""
    ============================================================
    The file path selected is not valid. The program asumes that 
    the file is stored in the top directory. If you wish to select 
    from the default options, write '--input default' as the command 
    line argument.
    ============================================================
    """)
    sys.exit(1)
else:
    input_message = """
    ============================================================
    {0} selected. 
    ============================================================
    Note that the file should be a txt file stored at the top 
    directory. The file should contain a header 'word' (see example 
    file) followed by a list of words, one word per line.
    ============================================================
    """ 
    print(input_message.format(args.input))

    dbname = args.input.split(".")[0]

    if args.stopwords: # if the user has provided their own filters
        filterbase = args.stopwords.split(".")[0]
        if not Path('databases/'+filterbase+'db').is_file():
            if Path(args.stopwords).is_file():
                print('Preparing stopword filters')
                prepare_data(args.stopwords)
                print('Creating stopword filter database')
                # Creates SQL database user_filters.db with header FILTER_WORD_FORMS
                user_filter_db = CorpusToSQL(corpus=args.stopwords, db_name='databases/'+filterbase)
                user_filter_db.create_db('FILTER_WORD_FORMS', 'filter')
            else:
                # Exit if the file provided doesn't exist
                print(f'The file <{args.stopwords}> does not exist. Aborting.')
                sys.exit(1)
    else:
        pass

    if not Path('databases/'+dbname+'.db').is_file():
        if Path(args.input).is_file():
            print('Preparing data.')
            prepare_data(args.input)
            print('Creating database.')
            # Creates SQL database (filename).db, with header LEXICON_WORD
            lexicon = CorpusToSQL(corpus=args.input, db_name='databases/'+dbname)
            lexicon.create_db('LEXICON_WORD', 'word')
        else:
            print(f'The file <{args.input}> does not exist or is in the wrong directory.')
    else:
        print(f'Database for file <{args.input}> already exists')