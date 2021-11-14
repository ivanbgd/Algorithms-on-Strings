import sys


class Node:
    """
    A Node contains starting point in text (relevant for both internal nodes and leaves),
    the substring end, and position in text at which the path to the leaf node begins, in case of leaf nodes only.
    It also contains the parent Node pointer and string depth.
    """
    def __init__(self, start=None, end=None, leaf_start=None, parent=None, string_depth=0):
        self.start = start
        self.end = end
        self.leaf_start = leaf_start
        self.parent = parent
        self.children = {}  # dict[char, Node]
        self.string_depth = string_depth


def create_new_leaf(node, text, suffix, length, leaf_start):
    leaf = Node(
        start=suffix+node.string_depth, end=length, leaf_start=leaf_start, parent=node, string_depth=length-suffix
    )
    node.children[text[leaf.start]] = leaf
    return leaf


def break_edge(node, text, start, offset, leaf_start):
    start_char = text[start]
    mid_char = text[start + offset]
    mid_node = Node(
        start=start, end=start+offset, leaf_start=leaf_start, parent=node, string_depth=node.string_depth+offset
    )
    mid_node.children[mid_char] = node.children[start_char]
    node.children[start_char].parent = mid_node
    node.children[start_char].start += offset
    node.children[start_char] = mid_node
    return mid_node


def suffix_array_to_suffix_tree(suffix_array, lcp_array, text):
    """
    Build suffix tree of the string text given its suffix array suffix_array and LCP array lcp_array.
        * start is the starting position (0-based) of the substring of text corresponding to the edge label
        * end is the first position (0-based) after the end of the substring corresponding to the edge label
    """
    length = len(text)
    root = Node()
    lcp_prev = 0
    current = root
    for i in range(length):
        suffix = suffix_array[i]
        while current.string_depth > lcp_prev:
            current = current.parent
        if current.string_depth == lcp_prev:
            current = create_new_leaf(current, text, suffix, length, i)
        else:
            start = suffix_array[i - 1] + current.string_depth
            offset = lcp_prev - current.string_depth
            mid_node = break_edge(current, text, start, offset, i)
            current = create_new_leaf(mid_node, text, suffix, length, i)
        if i < length - 1:
            lcp_prev = lcp_array[i]
    return root


def traverse_tree_recursive(tree):

    def traverse(tup):
        """Pre-order"""
        if tup[1] is None:
            return
        print(tup[1].start, tup[1].end)  # Visit.
        for char, child in sorted(tup[1].children.items()):
            traverse((char, child))

    for char, child in sorted(tree.children.items()):
        traverse((char, child))


def traverse_tree_pre_order(tree):
    root_children = sorted(tree.children.items(), reverse=True)
    stack = root_children
    while stack:
        node = stack.pop()[1]
        print("%d %d" % (node.start, node.end))
        for char, child in sorted(node.children.items(), reverse=True):
            stack.append((char, child))


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    sa = list(map(int, sys.stdin.readline().strip().split()))
    lcp = list(map(int, sys.stdin.readline().strip().split()))
    print(text)

    tree = suffix_array_to_suffix_tree(sa, lcp, text)

    traverse_tree_pre_order(tree)
