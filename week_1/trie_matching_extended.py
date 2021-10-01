import sys


# Example: {0:{'A':1,'T':2},1:{'C':3}}
def _build_trie(patterns):
    """Build and return trie based on "trie.py", by using dictionary of dictionaries.

        Add label "end" to each node to mark it as a node that ends a pattern, if True.
    """
    trie = dict()
    new_node_label = 0
    trie[new_node_label] = dict()
    trie[new_node_label]["end"] = False
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
                trie[new_node_label]["end"] = False
                current_node = trie[new_node_label]
                new_node_label += 1
            else:
                current_node = trie[existing_node_label]
        current_node["end"] = True
    return trie


def _prefix_trie_matching(text, trie):
    v = trie[0]
    i = 0
    symbol = text[i]
    pattern = []  # Pattern is spelled from root to v.
    while True:
        if v["end"]:  # 'v' ends a pattern.
            # print("".join(pattern))
            return "".join(pattern)
        elif v.get(symbol, None):
            pattern.append(symbol)
            v = trie[v[symbol]]
            i += 1
            symbol = text[i] if i < len(text) else None
        else:
            return None


def trie_matching(text, trie):
    positions = []
    for i in range(len(text)):
        result = _prefix_trie_matching(text[i:], trie)
        if result is not None:
            positions.append(i)
    return positions


def solve(text, n, patterns):
    tree = _build_trie(patterns)
    result = trie_matching(text, tree)
    result = list(set(result))
    result.sort()

    return result


text = sys.stdin.readline().strip()
n = int(sys.stdin.readline().strip())
patterns = []
for i in range(n):
    patterns.append(sys.stdin.readline().strip())

ans = solve(text, n, patterns)

sys.stdout.write(' '.join(map(str, ans)) + '\n')
