import sys
import numpy as np

"""
No checking for presence of "symbol".
This requires that we use a fixed alphabet, that is known in advance.
"""

"""
Old versions of Python don't guarantee the order of keys in a dictionary.
That's why I had to modify the loop in preprocess_bwt(). This refers to the "ALPHABET" dictionary.
I have to use mappings instead of integer "j" directly as index, which is slower.
"""

ALPHABET = {
    '$': 0,
    'A': 1,
    'C': 2,
    'G': 3,
    'T': 4,
}


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
    dim = len(bwt)

    starts = {}  # dict[str, int]: {character: index}
    occ_counts_before = np.empty(shape=(dim+1, len(ALPHABET)), dtype="int")  # 2D-array[int], dim+1 by len(ALPHABET)

    sorted_bwt = sorted(bwt)

    for char in ALPHABET:
        starts[char] = 0
    for i, char in enumerate(sorted_bwt):
        if starts[char] == 0:
            starts[char] = i

    # for j, alpha in enumerate(ALPHABET):
    #     counter = 0
    #     for i, char in enumerate(bwt):
    #         occ_counts_before[i][j] = counter
    #         if char == alpha:
    #             counter += 1
    #     occ_counts_before[dim][j] = counter

    for alpha in ALPHABET:
        index = ALPHABET[alpha]
        counter = 0
        for i, char in enumerate(bwt):
            occ_counts_before[i][index] = counter
            if char == alpha:
                counter += 1
        occ_counts_before[dim][index] = counter

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
            index = ALPHABET[symbol]
            top = starts[symbol] + occ_counts_before[top][index]
            bottom = starts[symbol] + occ_counts_before[bottom + 1][index] - 1
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
