import sys


def _create_suffixes(text):
    suffixes = []  # list[tuple(str, int)]]: List of tuples of suffixes and their starting positions in "text".
    for i in range(len(text)):
        suffixes.append((text[i:], i))
    return suffixes


def build_suffix_array(text):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    suffixes = _create_suffixes(text)
    suffixes.sort()
    result = [tup[1] for tup in suffixes]
    return result


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))
