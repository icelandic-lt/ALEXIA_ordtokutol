"""
This script leads the user through a series of questions that define
the format of the output. The initial settings ask the user to choose
between the demo version and a user-defined input version of the 
program. 
"""

import sys
import os
from pathlib import Path
from alexia.islensk_utgafa.find_texttype_freqs import texttype_freqs
from alexia.islensk_utgafa.txt_to_data import user_defined_freqlist
from alexia.islensk_utgafa.base_output import lemma_output, wordform_output
from alexia.islensk_utgafa.base_plus_other import lemmabase_wordforms, wordformbase_lemmas
from alexia.islensk_utgafa.collocation_output import user_defined_collocations, lemmas_collocations

# INITIAL SETTINGS

def icelandic_run_greeting():
    print("""
    ============================================================
    ALEXIA - Orðtökutól. 

    Velkomin í keyrsluhluta forritsins. Vinsamlegast gangið úr
    skugga um að uppsetning hafi verið framkvæmd og nauðsynlegir
    gagnagrunnar settir upp áður en haldið er áfram. 

    Viltu keyra demóútgáfu forritsins eða nota eigin gögn? 
    Demóútgáfuna má keyra annars vegar með Beygingarlýsingu
    islensks nútímamáls (BÍN) eða Nútímamálsorðabókinni (NMO). 
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
    (1) Eigin gögn
    (2) Demóútgáfa með BÍN
    (3) Demóútgáfa með NMO
        """)
    if initial_choice == "1":
        user_defined()
    elif initial_choice == "2":
        default_BIN()
    elif initial_choice == "3":
        default_dci()
    else:
        print("""
    ============================================================
    Þetta er ekki gildur valmöguleiki, reyndu aftur. 
    ============================================================
        """)
        initial_choice = default_or_user_defined()

# USER-DEFINED CHOICES

def enter_file():
    filename = input("""
    Skrifaðu slóðina að skjalinu og ýttu á ENTER.  
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

def enter_directory():
    directory = input("""
    Skrifaðu slóðina að möppunni og ýttu á ENTER. 
    """)
    if not Path(directory).is_dir():
        print(f"""
    ============================================================
    Mappan {directory} er ekki til. Reyndu aftur. 
    ============================================================
        """)
        directory = enter_directory()
    else:
        print(f"""
    ============================================================
    {directory} valin. 
    ============================================================
        """)
    return directory

def enter_output():
    output = number_input(2)
    if output == '1':
        print(f"""
    ============================================================
    Tíðnilisti valinn. 
    ============================================================
        """)
    elif output == '2':
        print(f"""
    ============================================================
    Orðstöðulykill valinn. 
    ============================================================
        """)    
    return output

def user_defined():
    if not Path('uttak/notendagogn/').is_dir():
            os.mkdir('uttak/notendagogn/')
    print("""
    ============================================================
    Eigin gögn valin. 
    ============================================================
    Skrifaðu fulla slóð skráarinnar sem inniheldur gagnagrunninn
    sem þú vilt nota (endar á .db).

    Dæmi: gagnagrunnar/ordasafn.db
    ============================================================
    """)
    database = enter_file()
    if database == 'None':
        print("""
    ============================================================
    Þú verður að gefa upp inntaksgagnagrunn. 
    ============================================================
        """)
        sys.exit(1)
    else:
        print(f"""
    ============================================================
    Inntaksgagnagrunnurinn: {database} valinn. 
    ============================================================
    Skrifaðu fulla slóð möppunnar þar sem málheildin er geymd
    sem á að bera saman við inntaksgagnagrunninn. Hafðu í huga
    að forritið gerir ráð fyrir að málheildin sé í einföldu 
    txt-sniði. 

    Dæmi: malheildir/txtmalheild
    ============================================================
        """)
    corpus = enter_directory()
    print(f"""
    ============================================================
    Málheildin: {corpus} valin.
    ============================================================
    Viltu nota stopporðalista til þess að útiloka viss orð frá
    niðurstöðunum? 

    Ef þú vilt nota stopporð, skrifaðu fulla slóð skjalsins sem
    inniheldur stopporðagagnagrunninn.
    Til að sleppa þessu skrefi, skrifaðu 'N'. 
    ============================================================
    """)
    filters = enter_file()
    if filters in ['N', 'n']:
        print(f"""
    ============================================================
    Engin stopporð valin.  
    ============================================================
        """)
    else:
        print(f"""
    ============================================================
    {filters} valið sem stopporðagagnagrunnur.  
    ============================================================
        """)
    
    print("""
    ============================================================
    Veldu tegund úttaks. 
    ============================================================
    (1) Tíðnilisti (orð, heildartíðni)
    (2) Tíðnilisti ásamt orðstöðulyklum fyrir hvert orð í niður-
    stöðunum (orð: heildartíðni [lykill 1, lykill 2...])

    Skrifaðu töluna sem samsvarar vali þínu og ýttu á ENTER.
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
    {number} er ekki gildur valmöguleiki. Reyndu aftur.
    ============================================================
            """)
            number = number_input(limit)
    except ValueError:
        print(f"""
    ============================================================
    Þú verður að skrifa tölu. Reyndu aftur. 
    ============================================================
        """)
        number = number_input(limit)

    return number

def prop_names():
    print("""
    ============================================================
    Viltu útiloka sérnöfn frá niðurstöðunum? 
    
    Þetta getur verið nytsamlegt þar sem sérnöfn eru almennt  
    mjög áberandi í orðalistunum. 

    (1) Útiloka sérnöfn
    (2) Halda sérnöfnum
    ============================================================
        """)
    prop_names = number_input(2)
    if prop_names == '1':
        print("""
    ============================================================
    Sérnöfn útilokuð. 
    ============================================================
        """)
    elif prop_names == '2':
        print("""
    ============================================================
    Sérnöfnum haldið. 
    ============================================================
        """)
    return prop_names

def lemmas_or_wordforms():
    print("""
    ============================================================
    Viltu nota lemmur (uppflettimyndir) eða orðmyndir (beygingar-
    myndir) sem grunnmynd í niðurstöðunum? 

    (1) Lemmur
    (2) Orðmyndir
    ============================================================
    """)
    base_form = number_input(2)
    if base_form == '1':
        print("""
    ============================================================
    Lemmur valdar. 
    ============================================================
        """)
    elif base_form == '2':
        print("""
    ============================================================
    Orðmyndir valdar. 
    ============================================================
        """)
    return base_form

def default_output(base_form):
    if base_form == '1': # lemmas
        print("""
    ============================================================
    Veldu tegund úttaksskjals.
    Skrifaðu töluna sem samsvarar vali þínu og ýttu á ENTER.

    (1) Tíðnilisti (lemma, tíðni) ásamt upplýsingum um það hvort
    nafnorð birtast oftar í eintölu eða fleirtölu. 
        
    (2) Tíðnilisti sem inniheldur allar orðmyndir sem standa
    með lemmunni (lemma, tíðni [orðmynd])
    
    (3) Tíðnilisti sem inniheldur tíðni lemmunnar innan vissra
    textategunda (lemma, heildartíðni: fréttir: tíðni, 
    íþróttir: tíðni...)

    (4) Tíðnilisti sem inniheldur orðstöðulykla (5 orð á lengd)
    fyrir lemmurnar (lemma : tíðni [orðstöðulykill])
    ============================================================
        """)
        choice = number_input(4)
    elif base_form == '2': # word forms
        print("""
    ============================================================
    Veldu tegund úttaksskjals. 
    Skrifaðu töluna sem samsvarar vali þínu og ýttu á ENTER.

    (1) Tíðnilisti (orðmynd, tíðni)

    (2) Tíðnilisti sem inniheldur allar lemmur sem standa með
    orðmyndinni (orðmynd, tíðni [lemma])
    ============================================================
        """)
        choice = number_input(2)
    return choice

def default_dci():
    if not Path('uttak/NMO/').is_dir():
        os.mkdir('uttak/NMO/')
    print("""
    ============================================================
    Þetta er NMO demóútgáfa ALEXIU. 

    Inntaksgögnin í þessari útgáfu eru úr Nútímamálsorðabókinni
    (NMO) og þau eru borin saman við gögn úr Risamálheildinni 
    (RMH). 
        
    Vinsamlegast gangið úr skugga um að uppsetningu gagnagrunna
    sé lokið með setup_icelandic.py og að RMH sé vistuð eins
    og dæmin sýna sem fylgja forritinu, þ.e.a.s. í slóðinni 
    ./malheildir/RMH/ með undirmöppunum CC_BY og MIM. 
    ============================================================
    Hvaða hluta RMH viltu nota til samanburðar við inntaksgögnin? 
            
    (1) Alla málheildina.
    (2) CC_BY (opni hluti RMH)
    (3) MÍM (Mörkuð íslensk málheild)
    (4) Ákveðin undirmappa (innan hvors hluta sem er)
    ============================================================
    """)   

    corpus_part = number_input(4)
    if corpus_part == "1":
        if not Path('malheildir/RMH/').is_dir():
            print(f"""
    ============================================================
    Mappan malheildir/RMH/ er ekki til. Vinsamlegast gangtu úr
    skugga um að RMH sé vistuð í sömu slóð og sýnidæmin.
    ============================================================
        """)     
        else:
            print(f"""
    ============================================================
    Öll RMH valin.  
    ============================================================
            """)
            propnames = prop_names()
            output = default_output('1')

            if propnames == '1': # excluded
                if output == '1': # plain freq list
                    lemma_output('NMO', "malheildir/RMH/", prop_names=False) 
                elif output == '2': # lemma freqs + all word forms
                    lemmabase_wordforms('NMO',"malheildir/RMH/", prop_names=False) 
                elif output == '3': # lemma freqs + text types
                    texttype_freqs('NMO',"malheildir/RMH/", prop_names=False) 
                elif output == '4':
                    lemmas_collocations('NMO',"malheildir/RMH/", prop_names=False)
            elif propnames == '2': # included
                if output == '1':
                    lemma_output('NMO', "malheildir/RMH/", prop_names=True)
                elif output == '2': 
                    lemmabase_wordforms('NMO',"malheildir/RMH/", prop_names=True)
                elif output == '3': 
                    texttype_freqs('NMO',"malheildir/RMH/", prop_names=True)
                elif output == '4':
                    lemmas_collocations('NMO',"malheildir/RMH/", prop_names=True)  

    elif corpus_part == "2":
        if not Path('malheildir/RMH/CC_BY').is_dir():
            print(f"""
    ============================================================
    Mappan malheildir/RMH/CC_BY/ er ekki til. Vinsamlegast gangtu 
    úr skugga um að RMH sé vistuð í sömu slóð og sýnidæmin.
    ============================================================
    """)             
        else:
            print(f"""
    ============================================================
    CC_BY valin. 
    ============================================================
            """)
            propnames = prop_names()
            output = default_output('1') 
            if propnames == '1': 
                if output == '1': 
                    lemma_output('NMO', "malheildir/RMH/CC_BY/", prop_names=False)
                elif output == '2': 
                    lemmabase_wordforms('NMO',"malheildir/RMH/CC_BY/", prop_names=False)
                elif output == '3': 
                    texttype_freqs('NMO',"malheildir/RMH/CC_BY/", prop_names=False)
                elif output == '4':
                    lemmas_collocations('NMO',"malheildir/RMH/CC_BY/", prop_names=False)

            elif propnames == '2': 
                if output == '1':
                    lemma_output('NMO',"malheildir/RMH/CC_BY/", prop_names=True)
                elif output == '2': 
                    lemmabase_wordforms('NMO',"malheildir/RMH/CC_BY/", prop_names=True)
                elif output == '3': 
                    texttype_freqs('NMO',"malheildir/RMH/CC_BY/", prop_names=True)
                elif output == '4':
                    lemmas_collocations('NMO',"malheildir/RMH/CC_BY/", prop_names=True)  

    elif corpus_part == "3":
        if not Path('malheildir/RMH/CC_BY').is_dir():
            print(f"""
    ============================================================
    Mappan malheildir/RMH/MIM/ er ekki til. Vinsamlegast gangtu 
    úr skugga um að RMH sé vistuð í sömu slóð og sýnidæmin.  
    ============================================================
            """)             
        else:        
            print(f"""
    ============================================================
    MIM valin. 
    ============================================================
            """)
            propnames = prop_names()
            output = default_output('1')
            if propnames == '1': 
                if output == '1': 
                    lemma_output('NMO',"malheildir/RMH/MIM/", prop_names=False)
                elif output == '2': 
                    lemmabase_wordforms('NMO',"malheildir/RMH/MIM/", prop_names=False)
                elif output == '3': 
                    texttype_freqs('NMO',"malheildir/RMH/MIM/", prop_names=False)
                elif output == '4':
                    lemmas_collocations('NMO',"malheildir/RMH/MIM/", prop_names=False)

            elif propnames == '2': 
                if output == '1':
                    lemma_output('NMO',"malheildir/RMH/MIM/", prop_names=True)
                elif output == '2': 
                    lemmabase_wordforms('NMO',"malheildir/RMH/MIM/", prop_names=True)
                elif output == '3': 
                    texttype_freqs('NMO',"malheildir/RMH/MIM/", prop_names=True)
                elif output == '4':
                    lemmas_collocations('NMO',"malheildir/RMH/MIM/", prop_names=True)

    elif corpus_part == "4":
        print(f"""
    ============================================================
    Undirmappa RMH valin. Vinsamlegast skrifaðu fulla slóð 
    möppunnar hér fyrir neðan og ýttu á ENTER. 
 
    Dæmi: malheildir/RMH/CC_BY/undirmappa
    ============================================================
            """)
        subdir = enter_directory()
        propnames = prop_names()
        output = default_output('1')
        if propnames == '1': 
            if output == '1': 
                lemma_output('NMO',subdir, prop_names=False)
            elif output == '2': 
                lemmabase_wordforms('NMO',subdir, prop_names=False)
            elif output == '3': 
                texttype_freqs('NMO',subdir, prop_names=False)
            elif output == '4':
                lemmas_collocations('NMO',subdir, prop_names=False)
        elif propnames == '2': 
            if output == '1':
                lemma_output('NMO',subdir, prop_names=True)
            elif output == '2': 
                lemmabase_wordforms('NMO',subdir, prop_names=True)
            elif output == '3': 
                texttype_freqs('NMO',subdir, prop_names=True)
            elif output == '4':
                lemmas_collocations('NMO',subdir, prop_names=True)

def default_BIN():
    if not Path('uttak/BIN/').is_dir():
        os.mkdir('uttak/BIN/')
    print("""
    ============================================================
    Þetta er BÍN demóútgáfa ALEXIU.

    Inntaksgögnin í þessari útgáfu eru úr Beygingarlýsingu
    íslensks nútímamáls (BÍN) og þau eru borin saman við gögn 
    úr Risamálheildinni (RMH). 
        
    Vinsamlegast gangið úr skugga um að uppsetningu gagnagrunna
    sé lokið með setup_icelandic.py og að RMH sé vistuð eins
    og dæmin sýna sem fylgja forritinu, þ.e.a.s. í slóðinni 
    ./malheildir/RMH/ með undirmöppunum CC_BY og MIM.    
    ============================================================
    Hvaða hluta RMH viltu nota til samanburðar við inntaksgögnin? 
            
    (1) Alla málheildina.
    (2) CC_BY (opni hluti RMH)
    (3) MÍM (Mörkuð íslensk málheild)
    (4) Ákveðin undirmappa (innan hvors hluta sem er)
    ============================================================
    """)
    
    corpus_part = number_input(4)
    if corpus_part == "1":
        if not Path('malheildir/RMH/').is_dir():
            print(f"""
    ============================================================
    Mappan malheildir/RMH/ er ekki til. Vinsamlegast gangtu úr
    skugga um að RMH sé vistuð í sömu slóð og sýnidæmin.
    ============================================================
        """)     
        else:
            print(f"""
    ============================================================
    Öll RMH valin. 
    ============================================================
            """)
            propnames = prop_names()
            base_form = lemmas_or_wordforms()
            output = default_output(base_form)

            if base_form == '1': # Lemmas
                if propnames == '1': # excluded
                    if output == '1': # plain freq list
                        lemma_output('BIN', "malheildir/RMH/", prop_names=False) 
                    elif output == '2': # lemma freqs + all word forms
                        lemmabase_wordforms('BIN',"malheildir/RMH/", prop_names=False) 
                    elif output == '3': # lemma freqs + text types
                        texttype_freqs('BIN',"malheildir/RMH/", prop_names=False) 
                    elif output == '4':
                        lemmas_collocations('BIN',"malheildir/RMH/", prop_names=False)

                elif propnames == '2': # included
                    if output == '1':
                        lemma_output('BIN', "malheildir/RMH/", prop_names=True)
                    elif output == '2': 
                        lemmabase_wordforms('BIN',"malheildir/RMH/", prop_names=True)
                    elif output == '3': 
                        texttype_freqs('BIN',"malheildir/RMH/", prop_names=True)
                    elif output == '4':
                        lemmas_collocations('BIN',"malheildir/RMH/", prop_names=True)

            elif base_form == '2': # Word forms
                if propnames == '1':
                    if output == '1':
                        wordform_output("malheildir/RMH/", prop_names=False)
                    elif output == '2':
                        wordformbase_lemmas("malheildir/RMH/", prop_names=False)
                elif propnames == '2':
                    if output == '1':
                        wordform_output("malheildir/RMH/", prop_names=True)
                    elif output == '2':
                        wordformbase_lemmas("malheildir/RMH/", prop_names=True)
    elif corpus_part == "2":
        if not Path('malheildir/RMH/CC_BY').is_dir():
            print(f"""
    ============================================================
    Mappan malheildir/RMH/CC_BY/ er ekki til. Vinsamlegast gangtu úr
    skugga um að RMH sé vistuð í sömu slóð og sýnidæmin.
    ============================================================
    """)             
        else:
            print(f"""
    ============================================================
    CC_BY valin. 
    ============================================================
            """)
            propnames = prop_names()
            base_form = lemmas_or_wordforms()
            output = default_output(base_form)
            if base_form == '1': # Lemmas        
                if propnames == '1': 
                    if output == '1': 
                        lemma_output('BIN',"malheildir/RMH/CC_BY/", prop_names=False)
                    elif output == '2': 
                        lemmabase_wordforms('BIN',"malheildir/RMH/CC_BY/", prop_names=False)
                    elif output == '3': 
                        texttype_freqs('BIN',"malheildir/RMH/CC_BY/", prop_names=False)
                    elif output == '4':
                        lemmas_collocations('BIN',"malheildir/RMH/CC_BY/", prop_names=False)

                elif propnames == '2': 
                    if output == '1':
                        lemma_output('BIN',"malheildir/RMH/CC_BY/", prop_names=True)
                    elif output == '2': 
                        lemmabase_wordforms('BIN',"malheildir/RMH/CC_BY/", prop_names=True)
                    elif output == '3': 
                        texttype_freqs('BIN',"malheildir/RMH/CC_BY/", prop_names=True)
                    elif output == '4':
                        lemmas_collocations('BIN',"malheildir/RMH/CC_BY/", prop_names=True)

            elif base_form == '2': # Word forms
                if propnames == '1':
                    if output == '1':
                        wordform_output("malheildir/RMH/CC_BY/", prop_names=False)
                    elif output == '2':
                        wordformbase_lemmas("malheildir/RMH/CC_BY/", prop_names=False)
                elif propnames == '2':
                    if output == '1':
                        wordform_output("malheildir/RMH/CC_BY/", prop_names=True)
                    elif output == '2':
                        wordformbase_lemmas("malheildir/RMH/CC_BY/", prop_names=True)            
    
    elif corpus_part == "3":
        if not Path('malheildir/RMH/MIM').is_dir():
            print(f"""
    ============================================================
    Mappan malheildir/RMH/MIM/ er ekki til. Vinsamlegast gangtu úr
    skugga um að RMH sé vistuð í sömu slóð og sýnidæmin.        
    ============================================================
            """)             
        else:        
            print(f"""
    ============================================================
    MÍM valin. 
    ============================================================
            """)
            propnames = prop_names()
            base_form = lemmas_or_wordforms()
            output = default_output(base_form)
            if base_form == '1': # Lemmas
                if propnames == '1': 
                    if output == '1': 
                        lemma_output('BIN',"malheildir/RMH/MIM/", prop_names=False)
                    elif output == '2': 
                        lemmabase_wordforms('BIN',"malheildir/RMH/MIM/", prop_names=False)
                    elif output == '3': 
                        texttype_freqs('BIN',"malheildir/RMH/MIM/", prop_names=False)
                    elif output == '4':
                        lemmas_collocations('BIN',"malheildir/RMH/MIM/", prop_names=False)

                elif propnames == '2': 
                    if output == '1':
                        lemma_output('BIN',"malheildir/RMH/MIM/", prop_names=True)
                    elif output == '2': 
                        lemmabase_wordforms('BIN',"malheildir/RMH/MIM/", prop_names=True)
                    elif output == '3': 
                        texttype_freqs('BIN',"malheildir/RMH/MIM/", prop_names=True)
                    elif output == '4':
                        lemmas_collocations('BIN',"malheildir/RMH/MIM/", prop_names=True)

            elif base_form == '2': # Word forms
                if propnames == '1':
                    if output == '1':
                        wordform_output("malheildir/RMH/MIM/", prop_names=False)
                    elif output == '2':
                        wordformbase_lemmas("malheildir/RMH/MIM/", prop_names=False)
                elif propnames == '2':
                    if output == '1':
                        wordform_output("malheildir/RMH/MIM/", prop_names=True)
                    elif output == '2':
                        wordformbase_lemmas("malheildir/RMH/MIM/", prop_names=True)

    elif corpus_part == "4":
        print(f"""
    ============================================================
    Undirmappa RMH valin. Vinsamlegast skrifaðu fulla slóð 
    möppunnar hér fyrir neðan og ýttu á ENTER. 
 
    Dæmi: malheildir/RMH/CC_BY/undirmappa
    ============================================================
            """)
        subdir = enter_directory()
        propnames = prop_names()
        base_form = lemmas_or_wordforms()
        output = default_output(base_form)
        if base_form == '1': # Lemmas
            if propnames == '1': 
                if output == '1': 
                    lemma_output('BIN',subdir, prop_names=False)
                elif output == '2': 
                    lemmabase_wordforms('BIN',subdir, prop_names=False)
                elif output == '3': 
                    texttype_freqs('BIN',subdir, prop_names=False)
                elif output == '4':
                    lemmas_collocations('BIN',subdir, prop_names=False)
            elif propnames == '2': 
                if output == '1':
                    lemma_output('BIN',subdir, prop_names=True)
                elif output == '2': 
                    lemmabase_wordforms('BIN',subdir, prop_names=True)
                elif output == '3': 
                    texttype_freqs('BIN',subdir, prop_names=True)
                elif output == '4':
                    lemmas_collocations('BIN',subdir, prop_names=True)
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

if __name__ == "__main__":
    icelandic_run_greeting()