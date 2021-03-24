from alexia.english_version.setup import english_setup_greeting
from alexia.english_version.run import english_run_greeting
from alexia.islensk_utgafa.setup_icelandic import icelandic_setup_greeting
from alexia.islensk_utgafa.run_icelandic import icelandic_run_greeting
from alexia.rename_directories import rename_dirs
import sys
import os

def bilingual_number_input():
    number = input("""
    Choose 1 for English / Veldu 2 fyrir íslensku: 
    """)
    try:
        if number not in ['1','2']:
            print(f"""
    ============================================================
    {number} is not a valid option. Please try again.
    {number} er ekki gildur valmöguleiki. Reyndu aftur.
    ============================================================
            """)
            number = bilingual_number_input()
    except ValueError:
        print(f"""
    ============================================================
    You must enter a number. Please try again.
    Þú verður að slá inn tölu. Reyndu aftur. 
    ============================================================
        """)
        number = bilingual_number_input()

    return number

def english_number_input():
    number = input("""
    Choose 1 to enter setup or 2 to run the program: 
    """)
    try:
        if number not in ['1','2']:
            print(f"""
    ============================================================
    {number} is not a valid option. Please try again.
    ============================================================
            """)
            number = english_number_input()
    except ValueError:
        print(f"""
    ============================================================
    You must enter a number. Please try again.
    ============================================================
        """)
        number = english_number_input()

    return number

def icelandic_number_input():
    number = input("""
    Veldu 1 til að fara í uppsetningu eða 2 til að keyra forritið:
    """)
    try:
        if number not in ['1','2']:
            print(f"""
    ============================================================
    {number} er ekki gildur valmöguleiki. Reyndu aftur.
    ============================================================
            """)
            number = icelandic_number_input()
    except ValueError:
        print(f"""
    ============================================================
    Þú verður að slá inn tölu. Reyndu aftur. 
    ============================================================
        """)
        number = icelandic_number_input()

    return number

def continue_or_quit(lang):
    if lang == 'ice':
        choice = input("""
    ============================================================
    Ýttu á C og ENTER til þess að halda áfram að keyra forritið. 
    Ýttu á Q og ENTER til að stöðva keyrsluna. 
    ============================================================        
        """)
        if choice in ['C', 'c']:
            icelandic_run_greeting()
        elif choice in ['Q', 'q']:
            sys.exit(1)
    elif lang == 'eng':
        choice = input("""
    ============================================================
    To continue to run the program, press C and ENTER.
    To quit, press Q and ENTER. 
    ============================================================        
        """)
        if choice in ['C', 'c']:
            english_run_greeting()
        elif choice in ['Q', 'q']:
            sys.exit(1)


def language_option():
    print("""
    ============================================================
    Please choose your language / Veldu tungumál.

    Note that if the directory names are not English, the process
    automatically renames them / Athugaðu að ef möppurnar sem 
    fylgja með pakkanum eru ekki á íslensku mun þetta ferli
    endurnefna þær

    Press 1 and ENTER for English.
    Ýttu á 2 og ENTER til að velja íslensku.
    ============================================================
    """)
    lang_opt = bilingual_number_input()
    if lang_opt == '1':
        print("""
    ============================================================
    To perform the necessary setup, press 1 and ENTER.
    To run the program, press 2 and ENTER.
    ============================================================        
        """)
        rename_dirs('eng')
        setup_or_run = english_number_input()
        if setup_or_run == '1':
            english_setup_greeting()
            continue_or_quit('eng')
        elif setup_or_run == '2':
            english_run_greeting()

    elif lang_opt == '2':
        print("""
    ============================================================
    Til að framkvæma nauðsynlega uppsetningu, ýttu á 1 og ENTER.
    Til að keyra forritið, ýttu á 2 og ENTER.
    ============================================================        
        """)
        rename_dirs('ice')
        setup_or_run = icelandic_number_input()
        if setup_or_run == '1':
            icelandic_setup_greeting() 
            continue_or_quit('ice')
        elif setup_or_run == '2':
            icelandic_run_greeting() 


language_option()