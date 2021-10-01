""" Build suffix tree directly, in form of a real tree

    Each suffix adds one leaf and at most one internal node to the suffix tree.
    A suffix tree may have more than one internal node on a path from root to a leaf. Example: "ATAAATG$" (Sample 3).
    Internal edges may be longer than one character. Example: "panamabananas".

    We store edges in nodes. More precisely, we store their starting position in text, and their length.
    We can print them easily this way AND we also save memory by storing only position and length instead of substring.
    Additionally, we store the position in text at which the path to the leaf node begins, in case of leaf nodes only.
    This is not required in this assignment.

    Sample cases:
    1) "A$" => "A$", "$"
    2) "ACA$" => "$", "A", "$", "CA$", "CA$"
    3) "ATAAATG$" => "AAATG$", "G$", "T", "ATG$", "TG$", "A", "A", "AAATG$", "G$", "T", "G$", "$"
    4) "AAA$" => "A", "A", "$", "$", "$", "A$" ["A", "$", "$", "A$", "AA$"]
"""

import sys
from collections import deque


class Node:
    """
    Node contains unique ID, starting point in text (relevant for both internal nodes and leaves),
    the substring length and position in text at which the path to the leaf node begins, in case of leaf nodes only.
    """

    def __init__(self, start=None, length=None, leaf_start=None):
        self.children = {}  # dict[char, Node]
        self.start = start
        self.length = length
        self.leaf_start = leaf_start

    def __str__(self):
        return f"start = {self.start}, length = {self.length}, leaf_start = {self.leaf_start}, " +\
               f"children.keys = {[key for key in self.children.keys()]}\n" +\
               f"\tchildren = " +\
               f"{[(k + ' ->', c.start, c.length, c.leaf_start, [k for k in c.children.keys()]) for k, c in self.children.items()]}"


def _build_tree(text):
    """Build suffix tree from text and return it"""
    suffix_length = 1 + len(text)
    root = Node()
    for i in range(len(text)):
        suffix = text[i:]
        suffix_length -= 1
        print(f"*** i = {i}; suffix = {suffix}; suffix length = {suffix_length}")
        current = root
        j = 0
        while j < suffix_length:
            print(f"* j = {j}, suffix[{j}] = {suffix[j]}, sub-suffix[{j}:] = {suffix[j:]}")
            print(f"current: {current}")
            try:
                print(f"Trying for '{suffix[j]}': ", end='')
                next_node = current.children[suffix[j]]
            except KeyError:
                new_leaf = Node(start=i+j, length=suffix_length-j, leaf_start=i)
                current.children[suffix[j]] = new_leaf
                print(f"KeyError; new_leaf: {new_leaf}")
                print(f"current: {current}")
                j += new_leaf.length  # break
            else:
                print(f"Success!\nnext_node: {next_node}")
                overlap = 0
                while suffix[j + overlap] == text[next_node.start + overlap] and overlap < next_node.length:
                    overlap += 1
                    print(f"overlap = {overlap}: '{suffix[j + overlap - 1]}'")
                if overlap == next_node.length:
                    current = next_node
                    j += overlap
                    print(f"overlap == next_node.length; j = {j}; overlap = {overlap}: '{suffix[j + overlap - 1]}'")
                    print(f"current: {current}")
                else:
                    new_internal = Node(start=next_node.start, length=overlap)
                    new_leaf = Node(start=i+j+overlap, length=suffix_length-j-overlap, leaf_start=i)
                    next_node.start += overlap
                    next_node.length -= overlap
                    new_internal.children[text[new_leaf.start]] = new_leaf
                    new_internal.children[text[next_node.start]] = next_node
                    current.children[text[new_internal.start]] = new_internal
                    print(f"current: {current}")
                    print(f"next_node: {next_node}")
                    print(f"new_internal: {new_internal}")
                    print(f"new_leaf: {new_leaf}")
                    assert next_node.length > 0
                    assert new_internal.length > 0
                    assert new_leaf.length > 0
                    break
            print("." * 30, flush=True)
        print("* edges:")
        traverse_tree(root, text)
        print("-" * 60)
        print("-" * 60)
    print("#" * 60)
    return root


def build_tree(text):
    """Build suffix tree from text and return it"""
    suffix_length = 1 + len(text)
    root = Node()
    for i in range(len(text)):
        suffix = text[i:]
        suffix_length -= 1
        print(f"*** i = {i}; suffix = {suffix}; suffix length = {suffix_length}")
        previous = root
        j = 0
        while j < suffix_length:
            print(f"* j = {j}, suffix[{j}] = {suffix[j]}, sub-suffix[{j}:] = {suffix[j:]}")
            print(f"previous: {previous}")
            try:
                print(f"trying for '{suffix[j]}': ", end='')
                current = previous.children[suffix[j]]
            except KeyError:
                new_leaf = Node(start=i+j, length=suffix_length-j, leaf_start=i)
                previous.children[suffix[j]] = new_leaf
                print(f"KeyError; new_leaf: {new_leaf}")
                print(f"previous: {previous}")
                j += new_leaf.length  # break
            else:
                print(f"Success!\ncurrent: {current}")
                overlap = 0
                while suffix[j+overlap] == text[current.start+overlap] and overlap < current.length + 1:
                    overlap += 1
                    print(f"overlap = {overlap}: '{suffix[j+overlap-1]}'")
                if overlap > current.length:
                    overlap = current.length
                    print(f"overlap > current.length; updated overlap = {overlap}: '{suffix[j + overlap - 1]}'")
                elif overlap < current.length:
                    diff = current.length - overlap
                    print(f"overlap < current.length; diff = {diff}")
                    new_internal = Node(start=current.start+diff, length=diff)
                    for child in current.children.values():
                        new_internal.children[text[child.start]] = child
                    current.children.clear()
                    current.children[text[new_internal.start]] = new_internal
                    current.length -= diff
                    print(f"new_internal: {new_internal}")
                    print(f"current: {current}")
                    assert new_internal.length > 0
                    assert current.length > 0
                    previous = current
                    j += overlap
                    continue
                try:
                    print(f" trying for '{suffix[j+overlap]}': ", end='')
                    _ = current.children[suffix[j+overlap]]
                except KeyError as e:
                    print(f"KeyError: {e}")
                    new_internal = Node(start=current.start, length=overlap)
                    current.start += overlap
                    current.length -= overlap
                    previous.children[text[new_internal.start]] = new_internal
                    new_internal.children[text[current.start]] = current
                    print(f"new_internal: {new_internal}")
                    print(f"current: {current}")
                    assert new_internal.length > 0
                    assert current.length > 0
                    previous = new_internal
                    j += overlap
                else:
                    print("Success!")
                    previous = current
                    next_node = current.children[suffix[j+overlap]]
                    new_overlap = 0
                    while suffix[j+overlap+new_overlap] == text[next_node.start+new_overlap] \
                            and new_overlap < suffix_length - j - overlap:
                        new_overlap += 1
                        print(f"new overlap = {new_overlap}: '{suffix[j+overlap+new_overlap-1]}'")
                    new_internal = Node(start=next_node.start, length=new_overlap)
                    next_node.start += new_overlap
                    next_node.length -= new_overlap
                    previous.children[suffix[j+overlap]] = new_internal
                    new_internal.children[text[next_node.start]] = next_node
                    print(f"new_internal: {new_internal}")
                    print(f"next_node: {next_node}")
                    assert new_internal.length > 0
                    assert next_node.length > 0
                    previous = new_internal
                    j += overlap + new_overlap
            print("." * 30)
        print("* edges:")
        traverse_tree(root, text)
        print("-" * 60)
        print("-" * 60)
    print("#" * 60)
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
