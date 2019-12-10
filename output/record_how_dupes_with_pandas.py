def hash_from_first(keywords, depth):
    keywords = str(keywords)
    set_keys = keywords.strip().split()[:depth]
    hashset = "".join(sorted(set_keys))
    return hashset

df['twofer'] = df['keywords'].apply(lambda x: hash_from_first(x, 2))

dupes = df[df.duplicated(['twofer'], keep=False)]
