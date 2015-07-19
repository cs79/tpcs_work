# global imports
import os
import codecs
from __future__ import division
import re
import string
from sklearn.feature_extraction.text import CountVectorizer

# go to working directory with raw files
os.chdir('C:/Users/Alex/Dropbox/Coursera/Capstone')

# read in all 3 files
f = codecs.open('Coursera-SwiftKey/final/en_US/en_US.twitter.txt', encoding='utf-8') # check encoding
rawtweets = f.read()            # as one big string
rawtweetlist = f.readlines()    # as a list of strings -- probably better
f.close()

f = codecs.open('Coursera-SwiftKey/final/en_US/en_US.blogs.txt', encoding='utf-8') # check encoding
rawblogs = f.read()            # as one big string
rawblogslist = f.readlines()    # as a list of strings -- probably better
f.close()

f = codecs.open('Coursera-SwiftKey/final/en_US/en_US.news.txt', encoding='utf-8') # check encoding
rawnews = f.read()            # as one big string
rawnewslist = f.readlines()    # as a list of strings -- probably better
f.close()

# create gigantic string (or do it in parts and build piecewise if taking too long)
'''
Try this:
1. using *lists from above, join the 3 lists into strings using ". " as a sep between lines
2. join all strings together using ". " as sep
'''
rawtext = ''  # output of doing the above

# clean the string
def clean_string():
    # stuff from other function in draft_prep goes here when it's ready
    return cleaned

cleantext = clean_string(rawtext)

# save it for later
f = open('cleaned_tweets.txt', 'w')
f.write(cleantext)
f.close()

# build the dictionary of ngrams - use functions from draft_prep when ready
def find_all_ngrams(input_string, max_n):
    vectorizer = CountVectorizer(ngram_range = (1, max_n))
    analyzer = vectorizer.build_analyzer()
    return(analyzer(input_string))

def simple_ngram_build(text, max_n = 4):
    if type(text) == list:
        text = " ".join(text)
    ngram_dict = dict()
    ngrams = find_all_ngrams(text, max_n)
    for ngram in ngrams:
        # ngram = " ".join([item for item in ngram]) # not needed with new find_all_ngrams function
        if ngram in ngram_dict:
            ngram_dict[ngram] += 1
        else:
            ngram_dict[ngram] = 1

    return ngram_dict

ngram_dict = simple_ngram_build(cleantext)

# build 2nd dict (trimmed -- n-1) for lookups
lookup_dict = [key[:-1] for key in ngram_dict.keys() where len(key) > 1]    # something like this - not tested yet

# prediction function
'''
This is the tricky part.  Some ideas:
1. CLEAN THE TEXT FIRST IN SAME MANNER USED TO CLEAN THE DICT, OTHERWISE IT WON'T MATCH
2. get the candidate keys (there is a fn for this in draft_prep)
3. for candidate keys:
    a. if in the lookup dict, get the frequency of all ngram_dict entries that pattern match the lookup
    b. [OPTIONAL] weight those frequencies by n-gram length (i.e. 2-gram freqs * 2)
    c. find which candidates have the highest (weighted) frequencies in the lookup
4. suggest the top 3 (weighted) frequency "follow-on-grams" based on candidates found in the lookup

$NUMBER markers represent an additional logic loop here, if used
'''
