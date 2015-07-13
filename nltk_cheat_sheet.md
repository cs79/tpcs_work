## NLTK cheat sheet

Text.concordance("string")          >   see matching string in context

Text.similar("string")              >   see words with "similar use" to string in the Text

Text.common_contexts(["s1", "s2"])  >   see contexts (surrounding words) shared by 2 or more strings

Text.dispersion_plot(["s1", "s2"])  >   see graphical dispersion of strings in a Text

len(Text) / len(set(Text))          >   a measure of "lexical richness" (comparable across Texts)

Text.count("string")                >   count occurrences of a specific string in a Text

FreqDist(Text)                      >   creates a FreqDist frequency distribution object from a Text

FreqDist.hapaxes()                  >   returns a list of hapaxes (single-occurrence words) from distr.

Text.collocations()                 >   returns collocations (unusually frequent bigrams)

Text.bigrams()                      >   returns list of bigrams as tuples







```python
from __future__ import division

def lexical_diversity(text):
    return len(text) / len(set(text))
```





<!---------------------------------------------------------------------------------------------->
as a cheat for getting the list of 1-grams, can use sorted(set(Text)) (but this won't give freqs)

Can use .count() for the freqs of 1-grams, doesn't seem to work for multi-word strings though

think about len(FreqDist.hapaxes()) / len(Text) versus len(FreqDist.hapaxes()) / len(set(Text)):

--> if hapaxes comprise a small percentage of the actual tokens but a large percentage of the frequency distribution, probably beneficial processing-wise to cut them from consideration, either altogether or from greater-than-1-grams

<!---------------------------------------------------------------------------------------------->
