import sys

# Slow.

"""
No checking for presence of "symbol".
This requires that we use a fixed alphabet, that is known in advance.

Optimizing preprocessing, from O(n**2) to O(n), by using the idea from the Counting Sort algorithm.
"""

ALPHABET = {
    '$': 0,
    'A': 1,
    'C': 2,
    'G': 3,
    'T': 4,
}

ALPHABET_TUPLE = ('$', 'A', 'C', 'G', 'T')


def _counting_sort(bwt):
    dim = len(bwt)

    count = [0] * len(ALPHABET)
    position = [0] * len(ALPHABET)
    occ_counts_before = [[0] * len(ALPHABET) for _ in range(dim+1)]  # dim+1 by len(ALPHABET)

    for char in bwt:
        count[ALPHABET[char]] += 1
    # print(f"count = {count}")

    position[ALPHABET['$']] = 0
    previous_char = ALPHABET_TUPLE[0]
    for j, char in enumerate(ALPHABET_TUPLE[1:], start=1):
        if count[ALPHABET[char]] > 0:
            position[ALPHABET[char]] = position[ALPHABET[previous_char]] + count[ALPHABET[previous_char]]
            previous_char = ALPHABET_TUPLE[j]
    # print(f"position = {position}")

    starts = position.copy()
    # print(f"starts = {starts}")

    sorted_bwt = [""] * dim
    for i, char in enumerate(bwt):
        sorted_bwt[position[ALPHABET[char]]] = char
        position[ALPHABET[char]] += 1
        for j in range(i + 1, dim + 1):
            occ_counts_before[j][ALPHABET[char]] += 1
    # print(f"sorted_bwt = {sorted_bwt}")
    # print(f"occ_counts_before = {occ_counts_before}")

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
            top = starts[ALPHABET[symbol]] + occ_counts_before[top][ALPHABET[symbol]]
            bottom = starts[ALPHABET[symbol]] + occ_counts_before[bottom + 1][ALPHABET[symbol]] - 1
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
