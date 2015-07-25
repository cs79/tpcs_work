# global imports
import os
import codecs
from __future__ import division
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
import random

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

# clean the string
def clean_string(input_text):
    cleaned = input_text.lower()
    cleaned = re.sub('["#$%&\()*+,/:;<=>@[\\]^_`{|}~]', '', cleaned)
    cleaned = re.sub(' [^ai1234567890][ |\.]', ' ', cleaned)
    cleaned = re.sub('\r\n', '. ', cleaned)
    cleaned = re.sub('\s+', ' ', cleaned)
    cleaned = re.sub('[!?]', '.', cleaned)
    cleaned = re.sub(' \.', '.', cleaned)
    cleaned = re.sub('\.+', '.', cleaned)
    cleaned = re.sub('[1234567890]+', '$NUMBER', cleaned)

    return cleaned

# takes a couple minutes
cleantext = clean_string(rawtext)
cleanlist = cleantext.split('. ')   # for use with complicated_ngram_build function below

# save cleantext for later -- may not be perfect as there is still room for improvement in clean_string
# but can use this as a baseline for now
f = codecs.open('cleaned_text.txt', 'w', encoding = 'utf-8')
f.write(cleantext)
f.close()

# build the dictionary of ngrams - use functions from draft_prep when ready
def find_all_ngrams(input_string, max_n = 3):
    vectorizer = CountVectorizer(ngram_range = (1, max_n), token_pattern = '[a-z]+[\'[a-z]+|[a-z]+]')
    analyzer = vectorizer.build_analyzer()
    return(analyzer(input_string))

# trying this function for getting ngram freqs first
# this may actually pose a bigger memory issue than the "complicated" function due to lack of an inner loop
def simple_ngram_build(text, max_n = 3):
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


#ngram_dict = simple_ngram_build(re.sub('\.', '', cleantext))    # dict that doesn't preserve semantic ordering
ngram_dict_semantic_ordering = complicated_ngram_build(cleanlist)   # takes about 10 mins to run w/ 4-grams

# build 2nd dict (trimmed -- n-1) for lookups -- takes about 4 mins (when max_n = 4 in ngram dict)
lookup_dict = [" ".join(key.split()[:-1]) if len(key.split()) > 1 else key for key in ngram_dict_semantic_ordering.keys()]



# even with n=3, dict still has over a 50 million keys -- trying to cut this down:
random.seed(1234)   # didn't run this on the version exported to R...
trunc_length = int(len(cleanlist) * 0.5) # can try different %s
random.shuffle(cleanlist)
truncated = cleanlist[:trunc_length]

trunc_ngram_dict = complicated_ngram_build(truncated)
# cutting 50% of the sentences at random cut about 83% of the keys, so this seems like a good tradeoff

# FOR EXPORTING FILES WITH PROPER LINE ENDINGS TO IMPORT INTO R
cleantext_R = re.sub('\. ', '\r\n', cleantext)
f = codecs.open('cleantext_R.txt', 'w', encoding = 'utf-8')
f.write(cleantext_R)
f.close()

dictkeys_R = ngram_dict_semantic_ordering.keys()
dictkeys_R = [key + '\r\n' for key in dictkeys_R]
dictkeys_R = ''.join(dictkeys_R)
f = codecs.open('ngramdictkeys_R.txt', 'w', encoding = 'utf-8')
f.write(dictkeys_R)
f.close()

dictvalues_R = ngram_dict_semantic_ordering.values()
dictvalues_R = [str(value) + '\r\n' for value in dictvalues_R]
dictvalues_R = ''.join(dictvalues_R)
f = codecs.open('ngramdictvalues_R.txt', 'w', encoding = 'utf-8')
f.write(dictvalues_R)
f.close()


allwords = ' '.join(cleanlist)

# TODO: build numbers dict
'''
Try something like this:
1. from rawtext, run a regex on anything that is a number
2. for each match, increment a number dict by 1 for that thing (similar to above fns)
3. reference this dict in predict function when predicting numbers
'''

# a function to find the key with the highest value
# edit this for my own purposes (something like this may be useful in predict function)
def keywithmaxval(d):
     """ a) create a list of the dict's keys and values;
         b) return the key with the max value"""
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

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
