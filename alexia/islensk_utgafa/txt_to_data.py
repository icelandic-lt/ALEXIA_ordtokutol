import glob
from alexia.sql.sql_lookup import SQLDatabase, SQLiteQuery
from progress.bar import IncrementalBar
import sys

def user_defined_freqlist(database,filterbase,corpus):
    """
    Iterates through a user-defined corpus and compares
    the results to a user-defined database, filtering out
    stopwords if the user has defined a stopword database.
    Returns a frequency word list.
    """
    db = SQLDatabase(db_name=database)
    txt_files = glob.glob(corpus+'/**/*.txt', recursive=True)
    print(filterbase)
    if filterbase not in ['n', 'N']:
        filters = SQLDatabase(db_name=filterbase)
    else:
        pass

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
            for w in words:
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
                        if not query.exists and not query_lower.exists: 
                            if len(w) > 1:
                                if w in outdict:
                                    outdict[w] += 1
                                else:
                                    outdict[w] = 1
                else:
                    query = SQLiteQuery(w,'word','LEXICON_WORD', cursor = db.cursor)                 
                    query_lower = SQLiteQuery(w.lower(),'word','LEXICON_WORD', cursor = db.cursor) 
                    if not query.exists and not query_lower.exists: 
                        if len(w) > 1:
                            if w in outdict:
                                outdict[w] += 1
                            else:
                                outdict[w] = 1
        filebar.next()
        sys.stdout.flush()
    filebar.finish()

    output_file = input("""
    ============================================================
    Skrifaðu það sem þú vilt að úttaksskjalið heiti með 
    endingunni .freq
 
    Dæmi: ordasafn.freq
    ============================================================
    """)

    with open('uttak/notendagogn/'+output_file, mode='w+') as outputfile:
        candidates = {k: v for k, v in sorted(outdict.items(),
                        key=lambda item: item[1], reverse=True)}
        for key, value in candidates.items():
            outputfile.write(key+': '+str(value)+ '\n')

    print(f"""
    ============================================================
    Úttaksskjalið {output_file} er tilbúið og má finna í 
    undirmöppunni uttak/notendagogn/
    ============================================================
    """)