######################################################################
2017/05/05 [23:37] Fri

Python script: word_count.py
######################################################################
Assuming python3 is up and running fine on the system:

[1] Install PyPDF2 and nltk:

pip install pypdf2
pip install nltk


[2] In python shell, download punkt:

import nltk
nltk.download('punkt')

[3] Change the filename in the script to your own pdf file: 
infile = 'Nature-2nd-Edited.pdf'

[4] Run the script!

==================================================
Result:
==================================================
Number of pages = 302
Number of tokens = 10439

   1: the             5529
   2: ,               4903
   3: of              3451
   4: .               2997
   5: to              2072
   6: and             2018
   7: in              1848


######################################################################
2017/05/28 [18:58] Sun
######################################################################

Based on Kai Ming's modification, the following changes are made:

[1]  The trival words are listed in a separate file ('wordfreq.py')
     for easier maintainence:

     A list of the top 5000 words is downloaded from 

     http://www.wordfrequency.info/free.asp

     and the first few dozens of words are used to eliminate the "trival
     words" from our word count.  It turns out that the list doesn't
     help much.  I still have to put in some words by hand (it's strange
     that words such as "is", "was", "are" aren't listed in the list
     of 5000.)


[2]  Word counts are given for each chapter as suggested by Kai Ming,
     and I further split it into sub-chapters (e.g. 1a and 1b).  The
     first and last page numbers for the first few chapters are, for
     some unknown reason, different from Kai Ming's (are we having
     different pdf files?)


[3]  Non-English words are eliminated.  The checking using 
     corpora/words from nltk takes way too long to run, so the 
     .isalpha() method is used instead.  You are welcome to try 
     the checking using corpora/words.  Simply download words by:

      import nltk
      nltk.download()

     and select Corpora -> words to download, and uncomment the
     following:

--------------------------------------------------
#  from nltk.corpus import words

         #  The use of corpora/words takes too long to run
         #  if not w in words.words(): continue
--------------------------------------------------

     and comment out the following:

         if not w.isalpha(): continue
      
[4]  The output is now saved into a file 'outfile' instead of stdout.

######################################################################
2017/05/31 [14:10] Wed
######################################################################

The following changes are made:

[1]  Refactored word_count.py and renamed as textbok.py

[2]  Tried to use nltk.words.words() to filter words. Found that some
     important names like 'Socrates', 'Glaucon' and 'Plato' are filtered.
     So, it may be better to use isalpha()

[3]  Sklearn package is used to count words. It is also used to eliminate
     stopwords.

[4]  Fixed wrong page number of each chapter

[5]  wordfreq.py is obsoleted

[6]  Added similarity_tf.py and similarity_tfidf to calculate cosine similarity
     between sample term paper and texts from textbook using 2 measures