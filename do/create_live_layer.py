import sys
import theseus
import bin.loadthem
from collections import defaultdict

if len(sys.argv) < 3:
    print("\n\tUsage: <cript> <keyword file location> depth_keys_to_associate")

class TheseusShip():
    def __init__(self, d_nodes, n_back):
       self.d_nodes = d_nodes
       self.back_node = back_node
       self.d_input_to_nodes = defaultdict(list)

    def absorb_nodes(self, d_nodes):
        """d_nodes is a dict, with name of book for key, and node with orderered
        high f keys as profile in theseus node for value.

        The purpose of this function is to create a dict, where the keys are possible
        incoming words, and the values are lists with references to which nodes recieve
        a head's up when the key arrives.  (observer pattern)
        """
        self.d_input_to_nodes = {      for name, kwrds in d_nodes.items() 
