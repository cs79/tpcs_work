import os
import codecs
from __future__ import division

os.chdir('C:/Users/Alex/Dropbox/Coursera/Capstone')

# try reading in a file as a raw string
f = codecs.open('Coursera-SwiftKey/final/en_US/en_US.twitter.txt', encoding='utf-8') # check encoding
rawtweets = f.read()            # as one big string
rawtweetlist = f.readlines()    # as a list of strings -- probably better
f.close()

#################################
# Text Cleaning / Preprocessing #
#################################
import re
import string

def clean_string(input_text):
    cleaned = input_text.lower()
    cleaned = re.sub('["#$%&\()*+,/:;<=>@[\\]^_`{|}~]', '', cleaned)
    cleaned = re.sub('\s+', ' ', cleaned)
    cleaned = re.sub('[!?]', '.', cleaned)
    cleaned = re.sub('\.+', '.', cleaned)
    cleaned = re.sub('[1234567890]+', '$NUMBER', cleaned)
    cleaned = re.sub(' [^ai1234567890][ |.]', '', cleaned)

    return cleaned

########################
# Regexes for cleaning #
########################

# lowercase everything
rawtext = rawtweets.lower()
# regex to strip punctuation except for ' . ! ? - (for hyphenated words)
rawtext = re.sub('["#$%&\()*+,/:;<=>@[\\]^_`{|}~]', '', rawtext)
# regex to trim whitespace down to 1 space
rawtext = re.sub('\s+', ' ', rawtext)
# re-sub . for other sentence-enders so that i can use . as a sentinel for splitting into lists
rawtext = re.sub('[!?]', '.', rawtext)
# trim sentinel periods down to a single .
rawtext = re.sub('\.+', '.', rawtext)
# eliminate numbers - maybe replace with a special sentinel, and keep a separate dict of number freqs
rawtext = re.sub('[1234567890]+', '$NUMBER', rawtext)
# eliminate single-letters that aren't A, I; single digits
rawtext = re.sub(' [^ai1234567890][ |.]', '', rawtext)


# get cleantext as a list of lists of words, each superset list is a "sentence" with semantic meaning to the ordering of the words
# each subset list is the words in those sentence broken into a list for ngram parsing
cleantext = [sentence.split() for sentence in rawtext.split('.')]



# save it for later
f = open('cleaned_tweets.txt', 'w')
f.write(cleantext)
f.close()

# now follow approach strategy

# solution to get ALL ngrams using CountVectorizer:
from sklearn.feature_extraction.text import CountVectorizer
def find_all_ngrams(input_string, max_n):
    vectorizer = CountVectorizer(ngram_range = (1, max_n))
    analyzer = vectorizer.build_analyzer()
    return(analyzer(input_string))


## stupidly simple alternative to the longer function below -- this appears to work ok now
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

## next idea: build max_n of 1 greater than what we want, then "trim" all n-grams by 1 gram and make a dict of the trimmed gram frequencies

## function to get candidate keys for lookup
def get_candidate_keys(input_text, max_input_length=3):
    # need to clean it too, probably should make a "clean text" function
    input_list = input_text.split()
    if len(input_list) > max_input_length:
        input_list = input_list[-max_input_length:]

    candidate_keys = [' '.join(input_list[-i:]) if len(input_list[-i:]) > 1 else input_list[-i] for i in range(len(input_list))]
    return(candidate_keys)

# test
test_input = "la laaa here we go ok this is longer than max"
test_output = get_candidate_keys(test_input)
# looks like it is working

def get_leading_keys(lookup_dict):
    leading_keys = [keys[:-1] for keys in lookup_dict.keys().split()]
    return leading_keys


'''
IF TIME PERMITS:
when predicting, allow for one gram (if n > 1) to be "anonymous" -
score all predictions with each 1-gram treated as any value (i.e. search dict for a pattern matching the n-1 with any pattern standing in for the anonymous one)
suggest highest scoring predictions
'''


# scratch files for testing the below:
test_text = 'this is a set of text to input. i\'m going to try this and see what happens.'
test_lookups = ['this', 'is', 'text to', 'input', 'to']
test_fdict = {'to input': 10, 'input': 12, 'text to input': 1}






# try an intermediary function to generate key matches
def key_match(candidate_key_list, valid_lookup_list, frequency_dict):
    matches = pd.DataFrame(columns=['next_word', 'freq_match', 'length_weight']) # df to return
    for candidate in candidate_key_list:
        if candidate not in valid_lookup_list:
            pass
        elif len(candidate.split()) <= 1:
            pass
        else:
            for key, value in frequency_dict.iteritems():
                if key.startswith(candidate):
                    matches = matches.append({'next_word': key.split()[-1], 'freq_match': value, 'length_weight': len(candidate.split())}, ignore_index=True)   # grab the last word

    return matches

# this needs more testing but on a simple test it appears to be at least sort of working...



# i think there is a bug in the function below but the logic of it is not horrible:

def predict_v2(input_text, max_n, candidate_key_list, valid_lookup_list, frequency_dict):
    prediction_keys = get_candidate_keys(input_text, max_n)
    top_predictions = key_match(prediction_keys, valid_lookup_list, frequency_dict)
    # do some weighting ... have added 3rd column to DF returned by key_match indicating length of matched key
    top_predictions['weighted_pred'] = top_predictions.freq_match ^ top_predictions.length_weight   # or something-- try a few things

    return list(top_predictions.sort('weighted_pred', ascending=False).next_word[:3])    # return top 3 weighted next words




## REMEMBER: We need to transform the input text to match the regexes used to clean the test used for our "model" otherwise it won't work well
def predict(input_text, lookup_dict, max_n):
    in_list = input_text.split()
    ngram_dict = lookup_dict
    to_predict = list()
    if len(in_list) == 0:
        return get_most_frequent_1gram()    # write a function to find the most frequent single word
    else:
        for i <= len(in_list) <= max_n:
            to_predict.append() # the trailing n-grams -- need to figure out how to do this, could write as a separate function

    # given new list of n-grams to_predict, look up those list items in the dict and weight the values according to approach strategy method (or something similar)

    predicted_word = # result of weighted prediction

    return predicted_word





###############
# timing test #
###############
from __future__ import division
testlength = 10000
test = rawtweets.split(" ")[:testlength]
%timeit testdict = simple_ngram_build(test)
# %timeit testdict = build_ngram_dict(test)
print('^^^ time taken to cover ' + str(testlength / len(test)) + ' percent of tweet corpus')



# this isn't actually currently giving what I want
def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


# function to build n-gram dict from a list of words (text)
def build_ngram_dict(text, max_n = 4):
    ngram_dict = dict()
    # cycle through all possible n-grams in range
    for startpoint in range(len(text)):
        # check if we can reach max_n from where we are, if not, trim max_n to fit
        if startpoint < len(text) - max_n:
            pass
        else:
            max_n = len(text) - startpoint
        # build n-grams from startpoint up to n_max
        current_string = text[startpoint:(startpoint + max_n)]
        current_ngrams = [find_ngrams(current_string, i) for i in range(1,max_n+1)]
        #flatten the list for parsing
        current_ngrams = [item for sublist in current_ngrams for item in sublist]
        #convert to string for substring matching
        current_string = " ".join(current_string)
    # given list of n-grams for our current string, count them and append counts to dict
        for ngram in current_ngrams:
            ngram = " ".join([item for item in ngram])# a clean version for substring matching
            ## could just make this loop increment the dictionary entry by 1 for each ngram in current set, probably a smarter idea than current double-counting implementation
            # if current ngram in dict, up the count
            if ngram in ngram_dict:
                ngram_dict[ngram] += current_string.count(ngram)
            # else, add it with count
            else:
                ngram_dict[ngram] = current_string.count(ngram)

    return ngram_dict

'''
above function currently works but double-counts things for appearing as sub-n-grams of a longer n-gram that is currently being counted.  I have probably overthought this, as usual.

Might be ok to just grab the frequencies directly when using the "find_ngrams" function (i.e. increment 1 each for each ngram found by the function and that's it)

'''


################################
# Pickling -- bad idea I think #
################################
# pickle our tweet dict for playing around with later, though honestly it didn't take as long as I thought it would to run the above code on the whole thing rather than the test subset
#pickling takes way too much space, and time -- easier to just re-run the dict, and it'll be faster / better once i do pre-processing on the text before even creating the dict (and if i fix the n-gram multi-counting)
# probably a way to export a dict as something else, too, rather than pickling -- there has to be a better way to do this
import pickle
output = open('pickles/tweetdict.pkl', 'wb')
pickle.dump(tweetdict, output)
loadfile = open('pickles/tweetdict.pkl', 'rb')
testload = pickle.load(loadfile)


'''
# nltk stuff that doesn't look promising:
-----------------------------------------
import nltk
from nltk.corpus import CorpusReader
from nltk import Text, FreqDist

tweetTokens = nltk.word_tokenize(rawtweets)
tweets = Text(rawtweets.read())
tweetFreqDist = FreqDist(tweets)
tweetHapaxes = tweetFreqDist.hapaxes()

tweets = Text('Coursera-SwiftKey/final/en_US/en_US.twitter.txt')
news = Text('Coursera-SwiftKey/final/en_US/en_US.news.txt')
blogs = Text('Coursera-SwiftKey/final/en_US/en_US.blogs.txt')
'''
