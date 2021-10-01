import sys

"""
This solution is generalized, in the sense that it doesn't depend on the alphabet. It works with any alphabet.
"""


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
    starts = {}  # dict[str, int]: {character: index}
    occ_counts_before = {}  # dict[str, list[int]]: {character: list[count]}

    sorted_bwt = sorted(bwt)
    for i, char in enumerate(sorted_bwt):
        try:
            starts[char]
        except KeyError:
            starts[char] = i

    alphabet = set(bwt)

    for alpha in alphabet:
        counter = 0
        count = []
        for char in bwt:
            count.append(counter)
            if char == alpha:
                counter += 1
        count.append(counter)
        occ_counts_before[alpha] = count

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
            if symbol in bwt[top:bottom+1]:
                top = starts[symbol] + occ_counts_before[symbol][top]
                bottom = starts[symbol] + occ_counts_before[symbol][bottom + 1] - 1
            else:
                # print(f"0. bottom = {bottom}, top = {top}")
                return 0
        else:
            # print(f"EMPTY. bottom = {bottom}, top = {top}")
            return bottom - top + 1
        i -= 1
    return None


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()

    # bwt = "smnpbnnaaaaa$a"

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
