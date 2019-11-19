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
import sys
import pandas as pd
import pryzm as pz
csv.field_size_limit(sys.maxsize)
error = pz.Pryzm().red


def create_nodes(path_content, ndic, back):
    """create all nodes, fill ndic with all line nodes and populate the back node"""
    try:
        df = pd.read_csv(path_content, encoding='ISO-8859-1')
    except Exception as e:
        error("Could not load dataframe from {}".format(path_content))
        error("Forwarded exception message: {}".format(e))
        sys.exit(1)

    for idx, row in enumerate(df.itertuples()):
        words = str(row.content).split()
        ndic[idx] = Node([words], row.name)
        back.merge(ndic[idx])
    return df

def generate_keywords(df, ndic, back):
    print(df.columns)
         
    df['keywords'] = df.apply(lambda row: " ".join(ndic[row['id']].create_profile(back, ratio=0.2)), axis=1)
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
