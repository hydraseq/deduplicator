"""
This script takes a bucket of extracted text files and generates the
theseus 'background' then gets the highest frequency words per book
against the background

Input:
    _source_file: string, path to file containing text content.  csv: id, name, full-text
    _ratio:       float, cutoff angle for keyword filter when comparing a source to background

Output:
    keyword_listing.csv:  file containing keyword output of neurons. csv: id, name, keywords (ranked in order left-right)

"""
import theseus.node as node
import csv
import sys
from collections import OrderedDict
csv.field_size_limit(sys.maxsize)

def load_all(fname):
    print("load_all, called with {}".format(fname))
    docs = []
    with open(fname, 'r') as source:
        for idx, line in enumerate(source):
            if idx % 100 == 0:
                print(idx)
            docs.append(line.split())
    return node.Node(docs, 'back')


def load_only(fname, _idx=-1):
    print("load_only: {}, _idx: {}".format(fname, _idx))
    assert isinstance(_idx, int), "idx must be an integer"

    docs = []
    with open(fname, 'r') as source:
        for idx, line in enumerate(source):
            if  idx == _idx:
                docs.append(line.split())
                name = line.split(',')[1]
                # print("Loaded line {}, named {}".format(idx, name))
                return node.Node(docs, name)

def load_both(fname):
    print("load both {}".format(fname))
    docs = []
    ndic = {}

    def _get_next(iter):
        #try:
        return next(iter)
        #except Exception as e:
        #    print("EXCEPTION: {}".format(str(e)))
        #    raise Exception("Exception getting an element")

    with open(fname, 'r') as source:

        j_rows = csv.DictReader(source)
        #row = next(j_rows)
        for row in j_rows:
            if not isinstance(row, OrderedDict):
                print("WHOA! type: {}".format(type(row)))
            if len(row) > 3:
                print("pop")
                continue
            elif len(row) == 3:
                words = row['content']
            else:
                raise Exception("batafuco!")
            sidx = row['id']
            name = row['name']
            idx = int(sidx)
            words = words.split()
            # print(idx, name, words)
            if idx % 100 == 0:
                print(idx)

            docs.append(words)
            ndic[idx] = node.Node([words], name)

    return node.Node(docs, 'back'), ndic



if __name__ == "__main__":

    _source_file = 'output/content.csv'
    _ratio = 0.2
    print("load_both from background and nodes from {}".format(_source_file))
    back, ndic = load_both(_source_file)
    print("done loading, start keyword extraction for {} nodes".format(len(ndic)))
    with open('output/keywords_listing.csv', 'w') as target:
        target.write("id,name,keywords\n")
        for idx, node in ndic.items():
            print(idx, node.name)
            target.write("{},{},{}\n".format(
                idx, node.name, " ".join(node.create_profile(back, ratio=_ratio))
                )
            )
            if idx % 100 == 0:
                print(idx)
