## General approach for text prediction model

### Data cleaning and preparation

1. Load data into a single string object for CLEANUP and tokenization
2. Clean the string using a bunch of regexes to strip out undesired stuff
3. tokenize into a frequency table
4. analyze frequency table for % of words remaining at "continuous" integer threshholds of frequencies for dropping a word
5. drop words that fall below the elbow of the threshhold
6. choice about profanity dropping or not
7. choice about keeping weird characters or not

8. (?) as part of step 1 above, insert a special character sequence / sentinel at the end of each tweet / instance of text / sentence even -- may be hard to tell where sentences end (try different regexes for patterns like `*._` and so forth)

### Text preprocessing

1. Get text as a flat string
2. Drop all non-apostraphe punctuation
3. Strip all whitespace down to 1 space
4. Make all letters lowercase (this will screw with things later)


### Frequency and sequence analysis

1. generate n-grams based on stopping character in (8) above -- can do this on a per-tweet or per-sentence basis (using a find_ngram type function and building up the dictionary stepwise per tweet or per sentence)
2. get n-gram frequencies

Could do this either as individual frequency tables for each n, or as one big table going up to whatever the max n ends up being (4?) but the first approach seems preferable perhaps...

Columns should maybe be progressive, like this:

(4-gram table example):

A big cat did | something | freq.
A big cat did | sth. else | freq.
A big cat did | &so forth | freq.

So that the table itself encodes the frequency of the subsequent words -- requires doing n-grams of n+1 and then splitting.  Possibly tricky / costly to loop through the actual frequencies, as well.

POSSIBLY BETTER APPROACH:

Rather than using frequency TABLES, use a set of dicts of lists of tuples, where the key is an n-gram, and the value is a list of tuples where the tuples are subsequent words found following that n-gram, along with their frequencies.  Probably faster for lookup but maybe less efficient for just getting the frequencies in the first place?  Not sure.  This seems like a promising avenue though.

3. MAKE SURE THESE ARE GETTING WRITTEN TO SOME OUTFILE SO THAT TIME SPENT CRUNCHING FREQUENCIES DOESN'T GET TOTALLY WASTED.

**Creation of these tables can probably all be done in Python faster than can be done in R / tm**

### Creating some kind of predictive model

Using the "progressive table" approach above, the initial idea would be that the model uses some sort of hierarchical loop like this:

1. check how long the current sequence is in words (m <- len(sequence))
2. for n < m:
    get top frequency "next" item for n-gram + frequency of that item + frequency of that n-gram (tuple)
    compare "next" items and if any match, calc the weighted frequency
    calc frequency of all items as a list of tuples
    assign a var an ordered list of tuples by weighted frequency

3. suggest the top 3 items in order of descending weighted frequency

ADDENDUM / CHANGE TO THIS:

1. take the top 3 items (or some other number) for EACH n-gram
2. weight the frequency scores via the combination method in the loop above, with an ADDITIONAL multiplier based on the length of the n-gram used in the suggestion

rationale: a more specific n-gram should be ranked higher for prediction, as it matches a greater part of the text string we have entered; on the opposite side of the spectrum, a 1-gram match is not very helpful since it will predict on the basis of a lot of combined prior patterns, so should be downweighted

for simplicity's sake, use weight = n, so a 1-gram has a weight of 1, a 3-gram has a weight of 3, etc.

This could be a hyperparameter that gets tuned in a grid search fashion if I can model this as a parametric equation with calculated targets (the latter part of this would be annoying probably, and/or expensive timewise, but would only have to be done once and could leverage the frequency tables created above)

#### Creating a better model

TBD -- think about this problem in more depth.  The above approach is more "brute force"; there may be a more clever way to go about the actual problem of prediction.  Think about what a prediction actually IS.

### Plugging the model into shiny

Need to refresh on this one.  Hopefully generic saved tables can be plugged in to shiny as a data source.  Can host them somewhere if need be (dropbox).
