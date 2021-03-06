"""
This script takes a file of extracted text and generates the
theseus 'background' then gets the highest frequency words per book
against the background

Input:
    _source_file: string, path to file containing text content.  csv: id, name, full-text
    _ratio:       float, cutoff angle for keyword filter when comparing a source to background

Output:
    keyword_listing.csv:  file containing keyword output of neurons. csv: id, name, keywords (ranked in order left-right)

"""
from theseus.node import Node
import csv
import re
import sys
import pandas as pd
import pryzm as pz
csv.field_size_limit(sys.maxsize)
error = pz.Pryzm().red

pattern = re.compile('[\W_]+')

def create_nodes(path_content, ndic, back, ngrams=True):
    """create all nodes, fill ndic with all line nodes and populate the back node"""
    def _get_ngrams(words):
        def _ngrams(words, n):
            nwds = len(words)
            return ["|".join(words[idx-n:idx]) for idx in range(n, nwds+1)]
        bigrams = _ngrams(words, 2)
        trgrams = _ngrams(words, 3)
        return words + bigrams + trgrams
    # ==============================================
    try:
        df = pd.read_csv(path_content, encoding='ISO-8859-1')
    except Exception as e:
        error("Could not load dataframe from {}".format(path_content))
        error("Forwarded exception message: {}".format(e))
        sys.exit(1)

    df.reset_index()
    df.id = df.index
    for idx, row in enumerate(df.itertuples()):
        words = str(pattern.sub(' ', row.content)).lower().split()
        if ngrams:
            words = _get_ngrams(words)
        ndic[idx] = Node([words], row.name)
        back.merge(ndic[idx])
    df = df.drop('content', axis=1)
    return df

def generate_keywords(df, ndic, back):
    print(df.columns)
         
    df['keywords'] = df.apply(lambda row: " ".join(ndic[row['id']].create_profile(back, ratio=0.2)), axis=1)
    df['top05'] = df['keywords'].apply(lambda x: " ".join(str(x).split()[:5]))
    df['top10'] = df['keywords'].apply(lambda x: " ".join(str(x).split()[:10]))
    df['top15'] = df['keywords'].apply(lambda x: " ".join(str(x).split()[:15]))
    df['top20'] = df['keywords'].apply(lambda x: " ".join(str(x).split()[:20]))
    return df

if __name__ == "__main__":

    _source_file = 'output/content.csv'
    _ratio = 0.2
    print("load_both from background and nodes from {}".format(_source_file))
    ndic = {}
    back = Node()
    df = create_nodes(_source_file, ndic, back)
    print("done loading, start keyword extraction for {}:{} nodes".format(len(ndic), len(df)))
   
    df = generate_keywords(df, ndic, back)
    df.to_csv('output/keywords_listing.csv')
