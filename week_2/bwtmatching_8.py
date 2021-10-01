import sys

# Slow.

"""
No checking for presence of "symbol".
This requires that we use a fixed alphabet, that is known in advance.

Optimizing preprocessing, from O(n**2) to O(n), by using the idea from the Counting Sort algorithm.
"""

ALPHABET = ('$', 'A', 'C', 'G', 'T')


def _binary_search(array, elt):
    """Modified binary search on an array."""
    start = 0
    end = len(array) - 1

    while start <= end:
        mid = (start + end) // 2
        if elt == array[mid]:
            return mid + 1
        if elt < array[mid]:
            end = mid - 1
        else:
            start = mid + 1

    if start > end:
        return start


def _counting_sort(bwt):
    dim = len(bwt)

    count = {}
    position = {}
    occ_counts_before = {}  # dict[str, list[int]]: {character: list[count]}
    for char in ALPHABET:
        count[char] = 0
        position[char] = 0
        occ_counts_before[char] = []

    for char in bwt:
        count[char] += 1

    position['$'] = 0
    previous_char = ALPHABET[0]
    for j, char in enumerate(ALPHABET[1:], start=1):
        if count[char] > 0:
            position[char] = position[previous_char] + count[previous_char]
            previous_char = ALPHABET[j]

    starts = position.copy()

    sorted_bwt = [""] * dim
    for i, char in enumerate(bwt):
        sorted_bwt[position[char]] = char
        position[char] += 1
        occ_counts_before[char].append(i + 1)

    return starts, occ_counts_before


def preprocess_bwt(bwt):
    """
    Preprocess the Burrows-Wheeler Transform bwt of some text
    and compute as a result:
      * starts - for each character C in bwt, starts[C] is the first position
          of this character in the sorted array of
          all characters of the text.
      * occ_counts_before - for each character C in bwt and each position P in bwt,
          occ_counts_before[C][P] is the number of occurrences of character C in bwt
          from position 0 to position P inclusive.
    """
    starts, occ_counts_before = _counting_sort(bwt)
    # print(f"starts = {starts}")
    # print(f"occ_counts_before = {occ_counts_before}")
    return starts, occ_counts_before


def count_occurrences(pattern, bwt, starts, occ_counts_before):
    """
    Compute the number of occurrences of a string pattern in a text,
    given only Burrows-Wheeler Transform, bwt, of the text, and additional
    information we get from the preprocessing stage - starts and occ_counts_before.
    """
    dim = len(bwt)
    top = 0
    bottom = dim - 1
    i = len(pattern) - 1
    while top <= bottom:
        if i >= 0:
            # print(f"pattern = {pattern[:i+1]}")
            symbol = pattern[i]
            # print(f"\tpattern = {pattern[:i]}, symbol = {symbol}")
            top = starts[symbol] + _binary_search(occ_counts_before[symbol], top)
            bottom = starts[symbol] + _binary_search(occ_counts_before[symbol], bottom + 1) - 1
        else:
            # print(f"EMPTY. bottom = {bottom}, top = {top}")
            return bottom - top + 1
        i -= 1
    return 0


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()

    # Preprocess the BWT once, to get starts and occ_counts_before.
    # For each pattern, we will then use these precomputed values and
    # spend only O(|pattern|) to find all occurrences of the pattern
    # in the text instead of O(|pattern| + |text|).
    starts, occ_counts_before = preprocess_bwt(bwt)
    occurrence_counts = []
    for pattern in patterns:
        # print(f"\nNEW PATTERN: {pattern}")
        occurrence_counts.append(count_occurrences(pattern, bwt, starts, occ_counts_before))
    # print(f"\nbwt = '{bwt}', pattern_count = {pattern_count}, patterns = {patterns}\noccurrence_counts = {occurrence_counts}\n")
    print(' '.join(map(str, occurrence_counts)))
