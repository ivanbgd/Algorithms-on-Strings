""" Build suffix tree directly, in form of a real tree

    Each suffix adds one leaf and at most one internal node to the suffix tree.
    A suffix tree may have more than one internal node on a path from root to a leaf. Example: "ATAAATG$" (Sample 3).
    Internal edges may be longer than one character. Example: "panamabananas$".

    We store edges in nodes. More precisely, we store their starting position in text, and their length.
    We can print them easily this way AND we also save memory by storing only position and length instead of substring.
    Additionally, we store the position in text at which the path to the leaf node begins, in case of leaf nodes only.

    Sample cases:
    1) "A$" => "A$", "$"
    2) "ACA$" => "$", "A", "$", "CA$", "CA$"
    3) "ATAAATG$" => "AAATG$", "G$", "T", "ATG$", "TG$", "A", "A", "AAATG$", "G$", "T", "G$", "$"
    4) "AAA$" => "A", "$", "$", "A", "$", "A$"

    This solution is generalized, in the sense that it doesn't depend on the alphabet.
    The implementation is general because it uses a dictionary for children, where the order between them
    is not defined. This has nothing to do with the order of insertion into the dictionary.
    Rather, we mean the comparison order, which is lexicographical (alphabetical).
    The comparison order becomes important when we want to create a Suffix Array from a Suffix Tree.
    Still, that problem is solvable externally to the tree.
"""

import sys
from collections import deque


class Node:
    """
    A Node contains the starting point in text (relevant for both internal nodes and leaves),
    the substring length, and position in text at which the path to the leaf node begins, in case of leaf nodes only.
    """

    def __init__(self, start=None, length=None, leaf_start=None):
        self.children = {}  # dict[char, Node]
        self.start = start
        self.length = length
        self.leaf_start = leaf_start


def build_tree(text):
    """Build suffix tree from text and return it"""
    suffix_length = 1 + len(text)
    root = Node()
    for i in range(len(text)):
        suffix = text[i:]
        suffix_length -= 1
        current = root
        j = 0
        while j < suffix_length:
            try:
                next_node = current.children[suffix[j]]
            except KeyError:
                new_leaf = Node(start=i+j, length=suffix_length-j, leaf_start=i)
                current.children[suffix[j]] = new_leaf
                j += new_leaf.length  # break
            else:
                overlap = 0
                while suffix[j+overlap] == text[next_node.start+overlap] and overlap < next_node.length:
                    overlap += 1
                if overlap == next_node.length:
                    current = next_node
                    j += overlap
                else:
                    new_internal = Node(start=next_node.start, length=overlap)
                    new_leaf = Node(start=i+j+overlap, length=suffix_length-j-overlap, leaf_start=i)
                    next_node.start += overlap
                    next_node.length -= overlap
                    new_internal.children[text[new_leaf.start]] = new_leaf
                    new_internal.children[text[next_node.start]] = next_node
                    current.children[text[new_internal.start]] = new_internal
                    break
    return root


def _traverse_tree_recursive(tree, text):

    def traverse(node, text):
        """Pre-order"""
        if node is None:
            return
        print(text[node.start:node.start+node.length])  # Visit.
        for child in node.children.values():
            traverse(child, text)

    for child in tree.children.values():
        traverse(child, text)


def _traverse_tree_level_order(tree, text):
    q = deque()
    for child in tree.children.values():
        q.append(child)
    while q:
        node = q.popleft()
        print(text[node.start:node.start+node.length])
        for child in node.children.values():
            q.append(child)


def _traverse_tree_dfs_(tree, text):
    stack = list()
    for child in tree.children.values():
        stack.append(child)
    while stack:
        node = stack.pop()
        print(text[node.start:node.start+node.length])
        for child in node.children.values():
            stack.append(child)


def _traverse_tree_dfs(tree, text):
    stack = list()
    stack.append(tree)
    while stack:
        node = stack.pop()
        for child in node.children.values():
            print(text[child.start:child.start+child.length])
            stack.append(child)


def traverse_tree(tree, text):
    """Traverse tree and return all its edges using text"""
    # We are not printing root!
    if tree is None:
        return
    _traverse_tree_level_order(tree, text)


def build_suffix_tree(text):
    """
    Build a suffix tree of the string text and return a list
    with all of the labels of its edges (the corresponding
    substrings of the text) in any order.
    """
    tree = build_tree(text)
    traverse_tree(tree, text)


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    build_suffix_tree(text)
