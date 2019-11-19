import pandas as pd
import sys

source_path = 'output/keywords_listing.csv'

df = pd.read_csv(source_path)

base, confidence, signal = None, None, None
if len(sys.argv) < 4:
    print("search_match.py base:word1,word2,word3 confidence:20 signal:5")
    sys.exit(0)
else:
    for arg in sys.argv[1:]:
        print("ARG:", arg)
        key, val = arg.split(':')
        if key == 'confidence': confidence = int(val)
        if key == 'signal': signal = int(val)
        if key == 'base': base = set(val.split(','))

if signal > len(base):
    print("** Resetting signal to be length of base!")
    signal = len(base)

df = df[df['keywords'].apply(
    lambda x: True if len(set(str(x).split()[:confidence]).intersection(base)) >= signal else False)]

print(df[['id','name','keywords']].head(20))

from collections import Counter
ct = Counter()
def countem(_ct, st):
    _ct.update(str(st).split())
    return st 

df['keywords'].apply(lambda x: countem(ct, x))
print(df.columns)
word_hits = ct.most_common()[:confidence]
for word, count in word_hits[:signal]:
    print(count, '\t', word)
print(word_hits[signal:])
