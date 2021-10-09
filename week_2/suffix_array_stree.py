import sys

# Slow.

"""
This solution is NOT generalized, in the sense that it does depend on the alphabet.
This is because we need to maintain an order of visiting child nodes when traversing the tree for the purpose of
printing the leaf nodes' starting positions in text.
The tree itself is general. I could have built it differently, where it would have taken the alphabet into account,
and maintain the order of the children, but I have borrowed my own implementation of the Suffix Tree from Week 1.
The implementation is general because it uses a dictionary for children, where the order between them
is not defined. This has nothing to do with the order of insertion into the dictionary. We mean the comparison order,
which is lexicographical (alphabetical).
So, it was easier for me to make traversal take care of the order of visiting children, since it was possible to do it.

The order that we need in this problem is the "in-order" traversal of the tree.
We are not printing internal nodes (root included). We only print leaves. This makes it possible to use the "pre-order"
traversal of the tree, and modify it to take care of the order of visiting the children.
We use the iterative approach to traversing the tree.
"""


# ALPHABET = ('$', 'A', 'C', 'G', 'T')


class Node:
    """
    Node contains unique ID, starting point in text (relevant for both internal nodes and leaves),
    the substring length, and position in text at which the path to the leaf node begins, in case of leaf nodes only.
    """

    def __init__(self, start=None, length=None, leaf_start=None):
        self.children = {}  # dict[char, Node]
        self.start = start
        self.length = length
        self.leaf_start = leaf_start


def _build_tree(text):
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


def _traverse_tree_pre_order_(tree):
    """DFS pre-order, but modified to effectively emulate in-order

       Only the leaf nodes' starting positions in text are printed.
       Leaves are the only nodes to have those starting positions anyway.
    """
    result = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if node.leaf_start is not None:
            result.append(node.leaf_start)
        for _, child in sorted(node.children.items()):
            stack.append(child)
    result.reverse()
    return result


def _traverse_tree_pre_order(tree):
    """DFS pre-order, but modified to effectively emulate in-order

       Only the leaf nodes' starting positions in text are printed.
       Leaves are the only nodes to have those starting positions anyway.
    """
    result = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if node.leaf_start is not None:
            result.append(node.leaf_start)
        for _, child in reversed(sorted(node.children.items())):
            stack.append(child)
    return result


def build_suffix_array(text):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    tree = _build_tree(text)
    result = _traverse_tree_pre_order(tree)
    return result


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))
