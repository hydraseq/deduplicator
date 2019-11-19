import bin.loadthem

n_back, d_nodes = bin.loadthem.load_both('output/content.csv')

from collections import defaultdict
input_to_nodes = defaultdict(list)

print("begin iteration")
for id, node in d_nodes.items():
    profile = node.create_profile(n_back)
    for word in profile:
        input_to_nodes[word].append(node)

# at this point, input_do_nodes should be a dict with words as keys,
# and each word has as value a list, with references to all the nodes
# that take that key

print(len(input_to_nodes), "words used")

for word, l in input_to_nodes.items():
    if len(l) > 150: print(word, len(l))

# TODO:
# on input, propagate message to nodes in list.  This means each node
# has to have a way to keep track, or maybe the container does that
# but I think it will be easier for the node to do it.
