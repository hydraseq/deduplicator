import pandas as pd


class Duper:
    def __init__(self, fpath):
        self.df = pd.read_csv(fpath)

    def hash_it(self, depth):
        self.depth = depth
        self.df['hash'] = self.df['keywords'].apply(lambda x: self._hash_from_first(x, self.depth))
        self.df = self.df.sort_values(by='hash')
        self.df = self.df[['id', 'hash', 'name', 'keywords']]
        return self

    def get_dupes(self):
        self.dupes = self.df[self.df.duplicated(['hash'], keep=False)]
        self.dupes = self.dupes[['hash', 'name']]
        return self.dupes

    def _hash_from_first(self, keywords, depth):
        """Given a string of keywords, split it, take depth, sort it and return hash"""
        return "".join(sorted(str(keywords).strip().split()[:depth]))

if __name__ == "__main__":
    import sys
    try:
        fpath = sys.argv[1]
        depth = 2
    except:
        print("argument must be path to csv with keywords")
        sys.exit(1)

    duper = Duper(fpath)

    duper.hash_it(2)

    duper.get_dupes().head()

#
#    df = pd.read_csv(fpath)
#
#    df['twofer'] = df['keywords'].apply(lambda x: hash_from_first(x, depth))
#
#    df = df[['id', 'twofer', 'name', 'keywords']]
#
#    df = df.sort_values(by='twofer')
#    
#    dupes = df[df.duplicated(['twofer'], keep=False)]
#
#    dupes.to_csv("dupes.csv")
#
#    print(dupes.head())
