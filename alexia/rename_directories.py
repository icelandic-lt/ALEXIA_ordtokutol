import os

def rename_dirs(lang):
    if lang == 'ice':
        try:
            os.rename('corpora', 'malheildir')
            os.rename('databases', 'gagnagrunnar')
            os.rename('output', 'uttak')
            os.chdir('malheildir')
            os.rename('IGC', 'RMH')
            os.rename('txtcorpus', 'txtmalheild')
            os.chdir('RMH')
            os.rename('TIC', 'MIM')
            os.chdir('../txtmalheild')
            os.rename('subdirectory', 'undirmappa')
            os.chdir('../..')
        except FileNotFoundError:
            pass
    elif lang == 'eng':
        try:
            os.rename('malheildir', 'corpora')
            os.rename('gagnagrunnar', 'databases')
            os.rename('uttak', 'output')
            os.chdir('corpora')
            os.rename('RMH','IGC')
            os.rename('txtmalheild','txtcorpus')
            os.chdir('IGC')
            os.rename('MIM','TIC')
            os.chdir('../txtcorpus')
            os.rename('undirmappa','subdirectory')
            os.chdir('../..')
        except FileNotFoundError:
            pass