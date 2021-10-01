import heapq
import sys

"""
Heap Sort is not a stable sort, but this is easily solvable.
Namely, we can add ranks to letters, and that's it.
The ranks serve as tie-breakers. They help us preserve the order among same elements.
But, we need those ranks anyway in this problem, so even better. :)
In this particular case (problem), we add ranks to suffixes, not to letters, but it's okay.
"""


def _create_suffixes(text):
    suffixes = []  # list[tuple(str, int)]]: List of tuples of suffixes and their starting positions in "text".
    for i in range(len(text)):
        heapq.heappush(suffixes, (text[i:], i))
    return [heapq.heappop(suffixes) for _ in range(len(suffixes))]  # heap sort


def build_suffix_array(text):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    suffixes = _create_suffixes(text)
    result = [tup[1] for tup in suffixes]
    return result


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))
