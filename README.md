# ALEXIA - A Lexicon Aqusition Tool

ALEXIA is a command-line based corpus tool used for comparing a certain
vocabulary to that of a larger corpus or corpora. In order to maintain 
lexicons, dictionaries and terminologies, it is necessary to be able 
to systematically go through large amounts of text considered to be 
representative of the language or category in question in order to find
potential gaps in the data. ALEXIA provides an easy way to generate such 
candidate lists. 

In order to successfully run ALEXIA, the following steps are needed: 

**(1) Run the file setup.py through the command line**
This script provides the user with a setup of the necessary
databases for ALEXIA. The script takes two command line arguments:

--input (or -i) is a filename to be used to create a lexicon database
defined by the user. This argument is required, however, if the user
only wants to install the default options, the argument written should
be --input default. **Note that the file should be a txt-file stored 
in the top directory and should contain a header 'word' (see the example
file lexicon.txt), followed by a list of words, one word per line.**  

-- stopwords (or -sw) is a filename to be used to create a user-defined 
filter database, that is to say, a list of words that should be excluded
from the output file. This argument is optional. **This file should also
be a txt-file stored in the top directory, containing the header 'filter',
followed by a list of words, one word per line.**

If the default version is chosen, the user does not need to provide 
any further information. The file necessary for the Database of 
Icelandic Morphology is automatically downloaded and then an 
SQL-database is created. In the same step, an SQL-database is 
created from a list of pre-defined stop-words/filters collected 
from the IGC. This list includes common foreign words, typos, 
misspellings, OCR-errors, lemmatization errors etc. Note that
this database is created from the all_filters.txt file included
in the package. 

**(2) Run the file run.py through the command line**
This script leads the user through a series of questions that define
the format of the output. The initial settings ask the user to choose
between the demo version and a user-defined input version of the 
program. 

**Note that to successfully run the demo-version, the IGC must be stored
in the same directory as the example files provided. The top directory
includes a subdirectory corpora, which includes two subdirectories,
CC_BY and TIC. The user must make sure that the IGC data is stored 
in the same way.**

If the user-defined version is chosen, the user is asked to provide 
the path to the lexicon SQL-database to be compared to the input corpus. 
The user must then provide the path to a corpus in a plan txt-format.
Optionally, the user can provide a path to a stopword/filter database
to exclude certain words from the results. If such a database is not
needed, the user in stead writes 'None' as an input. The two available
output formats are:
 
- A list of words and their frequencies in the input corpus that do 
not appear in the lexicon database (nor the stopwords, if provided). 
The list is ordered by frequency in descending order. 

- The same list as described in the option above, except it also 
includes 5-word collocation examples from the corpus, sorted by
descending frequency. 

If the demo version is chosen, the user is taken through the process
step-by-step, choosing the output of their choice. The demo version
compares the Database of Icelandic Morphology to the Icelandic Gigaword
Corpus. After indicating which part of the IGC to be used for comparison, 
the user is asked whether or not to exclude proper names from the results,
if they want to use lemmas or word forms and which output format they want. 
The following options are available: 

- LEMMAS: 
- A list of lemmas and their frequencies in the IGC that do not appear 
in the DIM nor the pre-defined filters. The list is ordered by frequency
in descending order. Also included is information on the frequency of 
singular versus plural nouns. This can be useful for detecting lemmatization
errors (such as when the lemma is singular but only ever appears in the plural
form in actuality) or to determine if a word only exists in either form. 

- A list of lemmas and their frequencies in the IGC that do not appear in 
the DIM nor the pre-defined filters, ordered by descending frequency. Also
included are all word forms that appear with the lemma in the IGC. This can
be useful for determining if a word only appears in certain grammatical context 
(e.g. a fixed expression).  

- A list of lemmas and their frequencies in the IGC that do not appear in the
DIM nor the pre-defined filters, ordered by descending frequency. Also included 
are the individual frequencies of the lemma within certain types of text, e.g. 
business news, sports reports, legal reports etc. 

- WORD FORMS:
- A list of word forms and their frequencies in the IGC that do not appear
in the DIM nor the pre-defined filters. The list is ordered by frequency in 
descending order. 

- A list of word forms and their frequencies in the IGC that do not appear
in the DIM nor the pre-defined filters, ordered by descending frequency. Also
included are all the lemmas that appear with the word form in the IGC. This 
can be useful for determining whether a word form can belong to more than one
parts of speech and if there are errors in the lemmatization. 

An example of these files can be found in the output directory included in 
this pacakge. 

**ALEXIA is an open-source software which can easily be adapted for other
forms of corpora. The code includes comments meant to facilitate modification. 
We encourage anyone to make their own versions, suitable to their needs.**

__If any errors or problems occur while using ALEXIA, the user can contact Steinunn
Rut Friðriksdóttir at srf2@hi.is or Atli Jasonarson at atlijas@simnet.is__
