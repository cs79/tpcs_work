## Assuming we have cleantext and ngram_dict_semantic_ordering from draft_method file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from __future__ import division
# iPython command for my system
%matplotlib qt

## Step 0
# get additional columns for dataframe: 'n', 'lookup', 'next_word'

# TEST CODE BELOW:
# column 'n' code now seems to work
asdf = pd.DataFrame({'ngrams' : ['this', 'is', 'a', 'test', 'now a threegram', 'and 2gram', 'now a dupe'],
    'frequency' : [4, 10, 3, 20, 1, 1, 3]})
asdf['n'] = [len(value.split()) for value in asdf.ngrams.values]

# get leading, trailing as 2 new columns
# (below appears to work but not sure about processing time req'd for a big DF)
asdf['leading']  = [" ".join(value.split()[:-1]) if len(value.split()) > 1 else value for value in asdf.ngrams.values]
asdf['trailing'] = [value.split()[-1] if len(value.split()) >1 else 'NA' for value in asdf.ngrams.values]

## Step 0.5
# do the above for real data, not fake data
dict_df = pd.DataFrame(ngram_dict_semantic_ordering.items(), columns=['ngrams', 'frequency'])
dict_df['n'] = [len(value.split()) for value in dict_df.ngrams.values]

# FORK: get rid of frequency < 10 (determined analytically via plotting code below):
dict_df = dict_df[dict_df.frequency > 10]
# then get rid of all but the top few 1-grams to use as filler predictions
keeper_1grams = dict_df[dict_df.n == 1].sort('frequency', ascending=False)[:10]
dict_df = dict_df[dict_df.n > 1].append(keeper_1grams)

# now get leading, trailing
dict_df['leading'] = [" ".join(value.split()[:-1]) if len(value.split()) > 1 else value for value in dict_df.ngrams.values]
dict_df['trailing'] = [value.split()[-1] if len(value.split()) >1 else 'NA' for value in dict_df.ngrams.values]

# save this as a CSV or text file that R will be able to read and check the filesize
dict_df.to_csv('lookup_outfile.csv')
#alternatively pruned file via fork method:
dict_df.to_csv('alt_pruned_lookup.csv')
'''
STILL TO CLEAN HERE:
manually remove "number" as an entry since it is coming from my cleaning function

STILL TO FIX IN R:
clean the string in a way that will match my cleaned dict (try to reproduce my regexes in R)
see if scoring by exponentiating the frequency by N produces better results (right now score is using multiplication)
'''

# code to find cutoff point to use in the FORK above:
test = pd.DataFrame(columns=['freq', 'percentage'])
for i in range(0,1000, 5):
    pct = len(dict_df[dict_df.frequency < i]) / len(dict_df)
    test = test.append({'freq': i, 'percentage': pct}, ignore_index=True)

plt.plot(test.freq, test.percentage, 'bo')

# no_hapaxes = dict_df[dict_df.frequency > 1]
# no_hapaxes.to_csv('lookup_no_hapaxes.csv')      # 72 MB with a 10% sample of the original data


## Step 1
# graph falloff of % removal for stepped frequency:
'''NEED TO DO THIS ONLY FOR 1-GRAMS
- also can use new dict_df above instead of reconstructing the dict again here'''
falloff = pd.DataFrame(ngram_dict_semantic_ordering.items(), columns=['ngrams', 'frequency'])
falloff['n'] = [len(value.split()) for value in falloff.ngrams.values]
falloff_onegrams = falloff[falloff['n'] == 1]
#falloff['fdbyten'] = falloff.frequency // 10

# REPLACE RANGE VALUES WITH REASONABLE ONES FOR ACTUAL DATA / SAMPLE
# this code works though
test = pd.DataFrame(columns=['freq', 'percentage'])
for i in range(0,3910, 5):
    pct = len(falloff_onegrams.loc[falloff_onegrams['frequency'] < i]) / len(falloff_onegrams)
    test = test.append({'freq': i, 'percentage': pct}, ignore_index=True)

plt.plot(test.freq, test.percentage, 'bo')


## Step 2
# get list of of hapaxes and/or single words below elbow frequency (*10 if using floor divided version)
cutoff = 5  # or whatever, based on analysis of the graph above
low_freqs = [key for key in ngram_dict_semantic_ordering.keys() if len(key.split()) == 1 and ngram_dict_semantic_ordering[key] < cutoff]

# test = [key for key in testdict.keys() if len(key.split()) == 1 and testdict[key] < 200] # works now

## Step 3
# pop and replace things from (2) with '.'
# RETEST THIS CODE AND STEP 4 ALSO
low_freqs_purged = cleantext
for word in low_freqs:
    word = ' ' + word + ' '
    low_freqs_purged = re.sub(word, '.', low_freqs_purged)

## Step 4
# sub '.' for ' .'
low_freqs_purged = re.sub(' \.', '.', low_freqs_purged)
low_freqs_purged = re.sub('\.+', '.', low_freqs_purged)

## Step 5
# split into list using '. ' as Step
cleanlist = cleantext.split('. ')

## Step 6
random.seed(12345)
random.shuffle(cleanlist)
len(cleanlist)
# pick a reasonable # of sentences to use to build ngrams, keeping in mind that a 10 word sentence will yield 24 4-grams
truncated_length = int(len(cleanlist)*0.1)
train = cleanlist[:truncated_length]    # so we can use later sequences as test / validation

train_dict = complicated_ngram_build(train)

## Step 7
valid_lookups = [" ".join(key.split()[:-1]) if len(str(key).split()) > 1 else key for key in train_dict.keys()]

## Candidate Key generator
def get_candidate_keys(input_text, max_input_length=3):
    # need to clean it too, probably should make a "clean text" function
    input_list = input_text.split()
    if len(input_list) > max_input_length:
        input_list = input_list[-max_input_length:]

    candidate_keys = [' '.join(input_list[-i:]) if len(input_list[-i:]) > 1 else input_list[-i] for i in range(len(input_list))]
    return(candidate_keys)

## Key match function
# still needs testing in draft_prep
'''
per kevin: instead of using a complex key match function that requires multiple LU dicts,
just build a very basic LU dict that ONLY stores the key + top-scoring next word
(for each of 1, 2, 3-grams leading)
'''
## Prediction



# working on this in draft_prep
