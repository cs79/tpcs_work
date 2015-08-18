# global imports
import os, codecs, re, string, random
from __future__ import division
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# iPython command for my system
%matplotlib qt

# go to working directory with raw files
os.chdir('C:/Users/Alex/Dropbox/Coursera/Capstone')

# read in all 3 files
f = codecs.open('Coursera-SwiftKey/final/en_US/en_US.twitter.txt', encoding='utf-8') # check encoding
# rawtweets = f.read()            # as one big string
rawtweetlist = f.readlines()    # as a list of strings -- probably better
f.close()

f = codecs.open('Coursera-SwiftKey/final/en_US/en_US.blogs.txt', encoding='utf-8') # check encoding
# rawblogs = f.read()            # as one big string
rawblogslist = f.readlines()    # as a list of strings -- probably better
f.close()

f = codecs.open('Coursera-SwiftKey/final/en_US/en_US.news.txt', encoding='utf-8') # check encoding
# rawnews = f.read()            # as one big string
rawnewslist = f.readlines()    # as a list of strings -- probably better
f.close()

# create gigantic string (or do it in parts and build piecewise if taking too long)
rawlists = [rawtweetlist, rawblogslist, rawnewslist]
rawtext = '. '.join(['. '.join(rawlist) for rawlist in rawlists])  # output of doing the above

# clean the string (this version gets rid of numbers entirely with no replacement sentinel)
def clean_string(input_text):
    cleaned = input_text.lower()
    cleaned = re.sub('["#$%&\()*+,/:;<=>@[\\]^_`{|}~]', '', cleaned)
    cleaned = re.sub(' [^ai1234567890][ |\.]', ' ', cleaned)
    cleaned = re.sub('[1234567890+]\.[1234567890+]', '', cleaned)   # kill decimal numbers
    cleaned = re.sub('[1234567890]+', '', cleaned)
    cleaned = re.sub('\r\n', '. ', cleaned)
    cleaned = re.sub('\s+', ' ', cleaned)
    cleaned = re.sub('[!?]', '.', cleaned)
    cleaned = re.sub(' \.', '.', cleaned)
    cleaned = re.sub('\.+', '.', cleaned)

    return cleaned

# takes a couple minutes
cleantext = clean_string(rawtext)
cleanlist = cleantext.split('. ')
del rawtext
del rawlists

# build the dictionary of ngrams - use functions from draft_prep when ready
def find_all_ngrams(input_string, max_n = 3):
    vectorizer = CountVectorizer(ngram_range = (1, max_n), token_pattern = '[a-z]+[\'[a-z]*|[a-z]*]')
    analyzer = vectorizer.build_analyzer()
    return(analyzer(input_string))

# build ngrams one sentence at a time to preserve semantic integrity -- need to test this still
def complicated_ngram_build(input_list, max_n = 3):
    ngram_dict = dict()
    for sentence in input_list:
        current_ngrams = find_all_ngrams(sentence, max_n)
        for ngram in current_ngrams:
            if ngram == []:
                pass
            elif ngram in ngram_dict:
                ngram_dict[ngram] += 1
            else:
                ngram_dict[ngram] = 1

    return ngram_dict

# build frequency dictionary; takes about 10 minutes
ngram_dict_semantic_ordering = complicated_ngram_build(cleanlist, 4)

# build dataframe from our dictionary
dict_df = pd.DataFrame(ngram_dict_semantic_ordering.items(), columns=['ngrams', 'frequency'])
dict_df['n'] = [len(value.split()) for value in dict_df.ngrams.values]
# prune low frequency terms
dict_df = dict_df[dict_df.frequency > 10]
# then get rid of all but the top few 1-grams to use as filler predictions
keeper_1grams = dict_df[dict_df.n == 1].sort('frequency', ascending=False)[:10]
dict_df = dict_df[dict_df.n > 1].append(keeper_1grams)
# now get leading, trailing
dict_df['leading'] = [" ".join(value.split()[:-1]) if len(value.split()) > 1 else value for value in dict_df.ngrams.values]
dict_df['trailing'] = [value.split()[-1] if len(value.split()) >1 else 'NA' for value in dict_df.ngrams.values]

# write out for use in R:
dict_df.to_csv('lookup_outfile_no_numbers.csv')
