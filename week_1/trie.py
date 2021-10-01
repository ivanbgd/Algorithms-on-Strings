import sys


# Return the trie built from patterns
# in the form of a dictionary of dictionaries,
# e.g. {0:{'A':1,'T':2},1:{'C':3}}
# where the key of the external dictionary is
# the node ID (integer), and the internal dictionary
# contains all the trie edges outgoing from the corresponding
# node, and the keys are the letters on those edges, and the
# values are the node IDs to which these edges lead.
#
# External dictionary contains nodes, and the nodes' internal dictionaries contain their outgoing edges.
# Nodes are labeled by integers, uniquely.
# If a node is a leaf, i.e., it doesn't have an outgoing edge, it will contain an empty dictionary.
# So, we create a node by adding a new empty dictionary to it.
# In other words, whenever we create a node, we should create a dictionary and assign it to the node.
# If a node has an outgoing edge, we fill its dictionary. If not, its dictionary remains empty.
def build_trie(patterns):
    trie = dict()

    new_node_label = 0
    trie[new_node_label] = dict()
    new_node_label += 1
    root = trie[0]
    for pattern in patterns:
        current_node = root
        for current_symbol in pattern:
            try:
                existing_node_label = current_node[current_symbol]
            except KeyError:
                current_node[current_symbol] = new_node_label
                trie[new_node_label] = dict()
                current_node = trie[new_node_label]
                new_node_label += 1
            else:
                current_node = trie[existing_node_label]

    return trie


if __name__ == '__main__':
    patterns = sys.stdin.read().split()[1:]
    tree = build_trie(patterns)
    for node in tree:
        for c in tree[node]:
            print("{}->{}:{}".format(node, tree[node][c], c))
