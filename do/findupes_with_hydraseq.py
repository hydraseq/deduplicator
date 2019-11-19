"""
Process a csv containing id | title | keywords ranked by freq
and  insert the first X keywords per title as a sequence in a hydraseq
"""
import hydraseq
import csv
import sys
import os
import pryzm
csv.field_size_limit(sys.maxsize)
debug = False
def _debug(*wurdz):
    global debug
    if debug:
        print(wurdz)

def load_hydra(source_file, depth):
    """Given source_file, create hydra from a the first 'depth' keywords"""
    hydra = hydraseq.Hydraseq('_')

    with open(source_file, 'r') as source, open('output/ten.csv', 'w') as target:
       csv_src = csv.DictReader(source)
       for row in csv_src:
           if len(row['keywords'].split()) <= 1:
               continue
           name = row['name'].strip()
           short_version = " ".join( row['keywords'].split()[:depth] )
           target.write(",".join([ row['id'], row['name'], short_version+'\n' ]))
           _debug("    load_hydra: inserting {}".format(short_version+' 0_'+name))

           hydra.insert(short_version+' 0_'+name)
    _debug("    load_hydra: returning hydra with number of keys => ", len(hydra.columns.keys()))
    return hydra

def find_duplicates(hydra):
    """Search the output layer of hydra and return connected output by last link"""
    def get_output_neurons(hydra):
        output_cols = [output_col for key, output_col in hydra.columns.items() if key.startswith('0_')]
        return { neuron for output_col in output_cols for neuron in output_col }

    out_nrns = get_output_neurons(hydra)
    _debug("    find_duplicates: found {} out_nrns".format(int(len(out_nrns))))
    groups = []
    while out_nrns:
        neuron = out_nrns.pop()
        group = {neuron.key.replace('0_','')}
        n_peers = {n_next for n_last in neuron.lasts for n_next in n_last.nexts}
        n_peers.remove(neuron)
        if len(n_peers) > 0:
            _debug("    find_duplicates: we have n_peers to process! for {}".format(neuron.key))
        for n_peer in n_peers:
            group.add(n_peer.key.replace('0_',''))
            if not n_peer.key.startswith('0_'):
                raise Exception("last key should start with 0_, got {} while on {}".format(n_peer.key, neuron.key))
            out_nrns.remove(n_peer)

        if len(group) > 1: groups.append(group)

    _debug("    find_duplcates returning {} groups".format(len(groups)))
    return groups

if __name__ == "__main__":

    pz = pryzm.Pryzm()
    yellow = pz.yellow

    try:
        source_file = sys.argv[1]
        try:
            depth = int(sys.argv[2])
        except:
            depth = 5
            print("** Using default depth number of 5 **")
    except:
        yellow("arguments: <source csv> <depth of keywords>")
        sys.exit(1)

    dupe_count = []
    for idx in range(depth):
        hydra = load_hydra(source_file, idx)
        dups = find_duplicates(hydra)
        dupe_count.append(str(len(dups)))
    print("Dupe count: ", dupe_count)

    hydra = load_hydra(source_file, depth)
    dups = find_duplicates(hydra)

    total = 0
    for idx, dup in enumerate(dups):
        if len(dup) > 1:
            print(len(dup),"\t", " ".join(sorted(dup)))
        total += len(dup)
    print([len([node for node in nodes if (len(node.nexts) > 1)]) for _, nodes in hydra.d_depths.items()])
    yellow("==== hydra dup search ===")
    yellow("Proceeding with file "+source_file)
    yellow("Required dup depth: "+str(depth))
    yellow("Hydra with number of keys => "+str(len(hydra.columns.keys())))
    yellow("Number of dup sets: "+str(len(dups)))
    yellow("total number books involved: "+str(total))

def print_tree(node):
    if not node.nexts:
        return
    else:
        print("*"*node.depth, node.key, len(node.nexts))
        for n in node.nexts:
            print_tree(n)

#print_tree(hydra.n_init)
