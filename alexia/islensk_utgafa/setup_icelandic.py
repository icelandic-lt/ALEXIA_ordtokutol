"""
This script provides the user with a setup of the necessary
databases for ALEXIA. Icelandic version.
"""

import sys
from pathlib import Path
from alexia.prepare_data import prepare_data
from alexia.sql.corpus_to_sql import CorpusToSQL
from alexia.request_file import request_file
from alexia.dci_extractor import get_text_output
import time

def get_files(choice):
    if choice == 'nmo':
        request_file('https://repository.clarin.is/repository/xmlui/bitstream/handle/20.500.12537/94/islensk_nutimamalsordabok.zip?sequence=7&isAllowed=y',
        'islensk_nutimamalsordabok.zip', zipped=True) 

    if choice == 'bin':
        request_file('https://bin.arnastofnun.is/django/api/nidurhal/?file=SHsnid.csv.zip',
                    'SHsnid.csv.zip', zipped=True)

def icelandic_setup_greeting():
    current_python = sys.version_info[:2]
    required_python = (3, 6)

    if current_python < required_python:
        sys.stderr.write(f"""
    ============================================================
    Úrelt Python útgáfa.

    Þetta forrit reiðir sig á Python {required_python[0]}.{required_python[1]} og
    ofar en þú ert að nota Python {current_python[0]}.{current_python[1]}. Vinsamlegast 
    uppfærðu Python. 
    ============================================================
    """)
        sys.exit(1)

    print("""
    ============================================================
    Velkomin í uppsetningarhluta ALEXIU. Veldu einn af eftirfarandi
    möguleikum með því að skrifa samsvarandi tölu og ýta á ENTER. 

    (1) SJÁLFGEFIN UPPSETNING: Þetta ferli býr til tvo gagnagrunna
    sjálfkrafa. Þú getur valið um að setja upp Beygingarlýsingu
    íslensks nútímamáls (BÍN) eða Nútímamálsorðabókina (NMO), 
    ásamt stopporðagagnagrunni sem var búinn til út frá
    Risamálheildinni (RMH). Gangtu úr skugga um að skjalið 
    IGC_filters.txt sé vistað í aðalmöppu ALEXIU.   
    
    (2) NOTENDAUPPSETNING: Eftir að þessi valmöguleiki er valinn
    þarftu að skrifa slóð txt-skjals sem inniheldur orðalista, 
    sambærilegan við dæmiskjalið lexicon.txt sem fylgir með
    forritinu. Gangtu úr skugga um að skjalið innihaldi 
    fyrirsögnina 'word' og síðan orðalista þar sem eitt orð
    er í hverri línu (sjá dæmiskjal). Auk þessa er valkvæður
    möguleiki að skrifa inn slóð txt-skjals sem inniheldur 
    stopporðalista, þ.e.a.s. orð sem á að hunsa í niðurstöðum.
    ============================================================
    """)

    default_or_user_defined()


def default_or_user_defined():
    print("""
    ============================================================
    Skrifaðu töluna sem samsvarar vali þínu og ýttu á ENTER. 
    ============================================================
    """)

    initial_choice = input("""
    (1) Sjálfgefin uppsetning
    (2) Notendauppsetning
    """)

    if initial_choice == "1":
        default()

    elif initial_choice == "2":
        user_defined()
    else:
        print("""
    ============================================================
    Þetta er ekki gildur valmöguleiki. Reyndu aftur. 
    ============================================================
    """)
        initial_choice = default_or_user_defined()

def number_choice():
    choice = input("""
    ============================================================
    Skrifaðu töluna sem samsvarar vali þínu og ýttu á ENTER.
    ============================================================
    """)
    if choice not in ['1', '2']:
        print("""
    ============================================================
    Þetta er ekki gildur valmöguleiki. Reyndu aftur. 
    ============================================================
    """)
        choice = number_choice()
    
    return choice

def filter_database():
    filters = 'IGC_filters.txt'
    if not Path('gagnagrunnar/IGC_filters.db').is_file():
        if Path(filters).is_file():
            print("""
    Undirbýr stopporðagagnagrunn. 
            """)
            prepare_data(filters)
            print("""
    Býr til stopporðagagnagrunn.
            """)
            # Creates SQL database filters.db with header FILTER_WORD_FORMS
            filter_db = CorpusToSQL(corpus=filters, db_name='gagnagrunnar/IGC_filters')
            filter_db.create_db('FILTER_WORD_FORMS', 'filter')
        else:
            # Exit if IGC_filters.txt doesn't exist
            print(f"""
    Skjalið <{filters}> er ekki til. Hættir við uppsetningu. 
            """)
            sys.exit(1)
    else:
        print(f"""
    Stopporðagagnagrunnur er nú þegar til.
        """)   

def enter_file():
    filename = input("""
    Sláðu inn fulla slóð skjalsins:
    """)
    if filename in ['N', 'n']:
        print(f"""
    ============================================================
    Ekkert skjal valið. 
    ============================================================
        """)
    elif not Path(filename).is_file():
        print(f"""
    ============================================================
    Skjalið {filename} er ekki til. Reyndu aftur.
    ============================================================
        """)
        filename = enter_file()
    else:
        pass 
    return filename

def name_database():
    db_name = input("""
    ============================================================
    Skrifaðu inn nafnið sem þú vilt nota á gagnagrunninn þinn, 
    án endingarinnar .db

    Dæmi: ordasafn_gagnagrunnur
    ============================================================
    """)

    if Path('gagnagrunnar/'+db_name+'.db').is_file():
        print(f"""
    ============================================================
    Gagnagrunnur með nafninu {db_name}.db er nú þegar til. 
    Reyndu aftur.
    ============================================================
        """)
        db_name = name_database()
    else:
        pass
    return db_name

def default():
    sh_snid = 'SHsnid.csv'
    nmo_xml = 'islensk_nutimamalsordabok.xml'
    nmo = 'nmo_ordalisti.txt'

    print("""
    ============================================================
    Sjálfgefin uppsetning valin. Þú getur annað hvort sett upp
    gagnagrunn fyrir Beygingarlýsingu íslensks nútímamáls (BÍN)
    eða Nútímamálsorðabókina (NMO). Sláðu inn töluna sem samsvarar
    vali þínu og ýttu á ENTER. 

    (1) BÍN
    (2) NMO
    ============================================================
    """)

    choice = number_choice()

    if choice == '1':
        print("""
    ============================================================
    Beygingarlýsing íslensks nútímamáls valin. Vinsamlegast 
    bíddu á meðan uppsetning nauðsynlegra gagnagrunna fer fram.
    ============================================================    
        """)
        filter_database()
        if not Path('gagnagrunnar/bin_lemmur_ordmyndir.db').is_file():
            if not Path(sh_snid).is_file():
                print(f"""
    Hleð niður skjalinu <{sh_snid}> svo hægt sé að setja upp BÍN.
                """)
                get_files('bin')
            if Path(sh_snid).is_file():
                print("""
    Undirbýr BÍN gagnagrunn.
                """)
                prepare_data(sh_snid)
                print("""
    Setur upp BÍN gagnagrunn.
                    """)
                # Creates SQL database dim_lemmas_word_forms.db with header DIM_ELEMENT
                sh_snid = CorpusToSQL(corpus=sh_snid, db_name='gagnagrunnar/bin_lemmur_ordmyndir')
                sh_snid.create_relational_database('DIM_ELEMENT', 'lemma', 'word_form')
        else:
            print(f"""
    BÍN gagnagrunnur er þegar til.
            """)    
    elif choice == '2':
        print("""
    ============================================================
    Nútímamálsorðabókin er valin. Vinsamlegast bíddu á meðan 
    uppsetning nauðsynlegra gagnagrunna fer fram.
    ============================================================    
        """)
        filter_database()
        if not Path('gagnagrunnar/nmo.db').is_file():
            if not Path(nmo_xml).is_file():            
                print(f"""
    Hleður niður skjalinu <{nmo_xml}>.
                """)
                get_files('nmo')
                time.sleep(2)
                print(f"""
    Býr til skjalið <{nmo}> sem er nauðsynlegt til að klára uppsetningu.
                """)
                get_text_output('is')
                time.sleep(2)
            if Path(nmo).is_file():
                print("""
    Undirbýr NMO gagnagrunn. 
                """)
                prepare_data(nmo)
                print("""
    Býr til NMO gagnagrunn.
                """)
            else:
                print(f"""
    Býr til skjalið <{nmo}> sem er nauðsynlegt til að klára uppsetningu.
                """)
                get_text_output('is')
                print("""
    Undirbýr NMO gagnagrunn. 
                """)
                prepare_data(nmo)
                print("""
    Býr til NMO gagnagrunn.
                """)                
                # Creates SQL database dim_lemmas_word_forms.db with header DIM_ELEMENT
                nmo_db = CorpusToSQL(corpus=nmo, db_name='gagnagrunnar/nmo')
                nmo_db.create_db('DCI_ELEMENT', 'lemma')
        else:
            print(f"""
    NMO gagnagrunnur er þegar til. 
            """)    
    print("""
    ============================================================
    Sjálfgefinni uppsetningu er lokið. Gagnagrunnarnir eru í 
    undirmöppunni gagnagrunnar. Næsta skref er að keyra skrána
    run_icelandic.py úr skipanalínunni eða halda áfram ferlinu
    í main.py.  
    ============================================================
    """)


def user_defined():
    print("""
    ============================================================
    Skrifaðu fulla slóð skjalsins sem inniheldur orðalistann sem
    þú vilt bera saman við orðaforða málheildar.

    Hafðu í huga að slóðin þarf að byggjast á þessari möppu. 
    Skjal sem er geymt á skjáborðinu gæti til dæmis haft 
    eftirfarandi slóð: ../../Desktop/ordasafn.txt
    ============================================================
    """)

    db = enter_file()

    print("""
    Undirbýr gögn. 
    """)

    prepare_data(db)
    db_name = name_database()

    print("""
    Býr til gagnagrunn. 
    """)

    # Creates SQL database (db_name).db, with header LEXICON_WORD
    lexicon = CorpusToSQL(corpus=db, db_name='gagnagrunnar/'+db_name)
    lexicon.create_db('LEXICON_WORD', 'word')

    print("""
    ============================================================
    Ef þú vilt búa til gagnagrunn með orðum sem á að hunsa í 
    niðurstöðunum (stopporð), skrifaðu inn slóð skjals á txt-sniði 
    sem inniheldur fyrirsögnina 'filter' og lista af orðum þar sem
    eitt orð er í hverri línu (sjá IGC_filters.txt). 
  
    Hafðu í huga að slóðin þarf að byggjast á þessari möppu. 
    Skjal sem er geymt á skjáborðinu gæti til dæmis haft 
    eftirfarandi slóð: ../../Desktop/stoppord.txt    

    Ef þú vilt ekki búa til stopporðagagnagrunn, skrifaðu N og
    ýttu á ENTER.
    ============================================================
    """)

    sw_db = enter_file()

    if sw_db in ['n', 'N']:
        print("""
    ============================================================
    Notendauppsetningu lokið. Gagnagrunnarnir eru í undirmöppunni
    gagnagrunnar. Næsta skref er að keyra run_icelandic.py frá
    skipanalínu eða halda áfram ferlinu í main.py 
    ============================================================
    """)
    else:
        print("""
    Undirbýr stopporðagagnagrunn. 
        """)
        prepare_data(sw_db)
        
        sw_name = name_database()
        print("""
    Býr til stopporðagagnagrunn. 
        """)
        # Creates SQL database (sw_name).db with header FILTER_WORD_FORMS
        user_filter_db = CorpusToSQL(corpus=sw_db, db_name='gagnagrunnar/'+sw_name)
        user_filter_db.create_db('FILTER_WORD_FORMS', 'filter')
    
    print("""
    ============================================================
    Notendauppsetningu lokið. Gagnagrunnarnir eru í undirmöppunni
    gagnagrunnar.
    ============================================================
    """)

if __name__ == "__main__":
    icelandic_setup_greeting()