import sys

"""
It is the fastest to work with a pre-defined alphabet, obviously.
But, if we'd like to make our solution general, we could actually "find out" about the alphabet
by creating a set of "text" and then sorting that set in ascending order. This is how it's done here.
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
    return order[1:]


def pattern_matching_with_suffix_array(text, pattern, suffix_array):
    min_ind = 0
    max_ind = len(text)
    while min_ind < max_ind:
        mid_ind = (min_ind + max_ind) // 2
        if pattern > text[suffix_array[mid_ind]: min(suffix_array[mid_ind] + len(pattern), len(text))]:
            min_ind = mid_ind + 1
        else:
            max_ind = mid_ind
    start = min_ind

    max_ind = len(text)
    while min_ind < max_ind:
        mid_ind = (min_ind + max_ind) // 2
        if pattern < text[suffix_array[mid_ind]: min(suffix_array[mid_ind] + len(pattern), len(text))]:
            max_ind = mid_ind
        else:
            min_ind = mid_ind + 1
    end = max_ind - 1

    if start > end:
        return None
    else:
        return start, end


def find_occurrences(text, patterns, alphabet):
    occurrences = set()

    suffix_array = build_suffix_array(text + '$', alphabet)
    # print(f"suffix_array = {suffix_array}")
    for pattern in patterns:
        result = pattern_matching_with_suffix_array(text, pattern, suffix_array)
        # print(result)
        if result is not None:
            start, end = result
            for i in range(start, end + 1):
                pos = suffix_array[i]
                # print(pos)
                occurrences.add(pos)

    return occurrences


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()

    # alphabet = ALPHABET = ('$', 'A', 'C', 'G', 'T')
    # alphabet = sorted(set(text + '$'))

    text += '$'
    alphabet = sorted(set(text))
    # print(alphabet)

    occs = find_occurrences(text, patterns, alphabet)

    print(" ".join(map(str, occs)))
