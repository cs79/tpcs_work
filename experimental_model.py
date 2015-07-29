## Assuming we have cleantext and ngram_dict_semantic_ordering from draft_method file
import pandas as import pd
import numpy as np
import matplotlib.pyplot as plt

## Step 1
# graph falloff of % removal for stepped frequency:
falloff = pd.DataFrame(ngram_dict_semantic_ordering.items(), columns=['ngrams', 'frequency'])

plt.hist(falloff['frequency']//10, bins=100)    # something like this

## Step 2
# get list of of hapaxes and/or single words below elbow frequency (*10 if using floor divided version)
low_freqs = [key for key in ngram_dict_semantic_ordering.keys() if len(key.split()) == 1 and ngram_dict_semantic_ordering[key] < 40]

# test = [key for key in testdict.keys() if len(key.split()) == 1 and testdict[key] < 200] # works now

## Step 3
# pop and replace things from (2) with '.'
low_freqs_purged = cleantext
for word in low_freqs:
    low_freqs_purged = re.sub(word, '.', low_freqs_purged)

## Step 4
# sub '.' for ' .'
low_freqs_purged = re.sub('\ .', '\.', low_freqs_purged)

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

## Prediction



# working on this in draft_prep
