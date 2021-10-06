import sys

""" Generate BWT From the Suffix Array of a String

    This solution uses a fast algorithm from Weeks 3 & 4 - P2, "suffix_array_long.py",
    for generating suffix array of a string, and then it turns the SA into the BWT of the string
    using the idea from: http://web.stanford.edu/class/cs262/presentations/lecture4.pdf (16/33).
    We need to rotate left by one position to get a BWT from a SA.
"""


def sort_characters(text, alphabet):
    """Counting Sort"""
    dim = len(text)
    order = [0] * dim
    count = {k: 0 for v, k in enumerate(alphabet)}

    for char in text:
        count[char] += 1

    for j in range(1, len(alphabet)):
        count[alphabet[j]] += count[alphabet[j-1]]

    for i, char in reversed(tuple(enumerate(text))):
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


def build_suffix_array(text, alphabet):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    order = sort_characters(text, alphabet)
    klass = compute_char_classes(text, order)
    length = 1
    while length < len(text):
        order = sort_doubled(text, length, order, klass)
        klass = update_classes(order, klass, length)
        length *= 2
    return order


def bwt_from_suffix_array(text, suffix_array):
    bwt = [text[pos - 1] for pos in suffix_array]
    return "".join(bwt)


if __name__ == '__main__':
    text = sys.stdin.readline().strip()

    alphabet = sorted(set(text))
    suffix_array = build_suffix_array(text, alphabet)
    bwt = bwt_from_suffix_array(text, suffix_array)

    print(bwt)
