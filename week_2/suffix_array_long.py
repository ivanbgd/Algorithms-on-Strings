import sys

"""This is a solution to Weeks 3 & 4 - P 2."""

"""
It is the fastest to work with a pre-defined alphabet, obviously, like we do here.
But, if we'd like to make our solution general, we could actually "find out" about the alphabet
by creating a set of "text" and then sorting that set in ascending order.
"""

ALPHABET = ('$', 'A', 'C', 'G', 'T')


def sort_characters(text):
    """Counting Sort"""
    dim = len(text)
    order = [0] * dim
    count = [0] * len(ALPHABET)

    alphabet_indices = {k: v for v, k in enumerate(ALPHABET)}

    for char in text:
        count[alphabet_indices[char]] += 1

    for j in range(1, len(ALPHABET)):
        count[j] += count[j-1]

    # for i, char in reversed(tuple(enumerate(text))):
    for i in range(dim-1, -1, -1):
        char = text[i]
        count[alphabet_indices[char]] -= 1
        order[count[alphabet_indices[char]]] = i

    return order


def sort_characters_(text):
    """Counting Sort"""
    dim = len(text)
    order = [0] * dim
    count = {k: 0 for v, k in enumerate(ALPHABET)}

    for char in text:
        count[char] += 1

    for j in range(1, len(ALPHABET)):
        count[ALPHABET[j]] += count[ALPHABET[j-1]]

    for i, char in reversed(tuple(enumerate(text))):
    # for i in range(dim-1, -1, -1):
    #     char = text[i]
        count[char] -= 1
        order[count[char]] = i

    return order


def compute_char_classes(text, order):
    dim = len(text)
    klass = [0] * dim
    for i in range(1, dim):
        if text[order[i]] != text[order[i-1]]:
            klass[order[i]] = klass[order[i-1]] + 1
        else:
            klass[order[i]] = klass[order[i-1]]
    return klass


def sort_doubled(text, length, order, klass):
    dim = len(text)
    count = [0] * dim
    new_order = [0] * dim

    for i in range(dim):
        count[klass[i]] += 1
    for j in range(1, dim):
        count[j] += count[j-1]
    for i in range(dim-1, -1, -1):
        start = (order[i] - length + dim) % dim
        kl = klass[start]
        count[kl] -= 1
        new_order[count[kl]] = start
    return new_order


def update_classes(new_order, klass, length):
    n = len(new_order)
    new_class = [0] * n
    for i in range(1, n):
        current = new_order[i]
        previous = new_order[i-1]
        middle = (current + length) % n
        mid_prev = (previous + length) % n
        if klass[current] != klass[previous] or klass[middle] != klass[mid_prev]:
            new_class[current] = new_class[previous] + 1
        else:
            new_class[current] = new_class[previous]
    return new_class


def build_suffix_array(text):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    order = sort_characters(text)
    klass = compute_char_classes(text, order)
    length = 1
    while length < len(text):
        order = sort_doubled(text, length, order, klass)
        klass = update_classes(order, klass, length)
        length *= 2
    return order


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))
