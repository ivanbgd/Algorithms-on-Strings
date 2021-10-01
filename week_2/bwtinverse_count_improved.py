import sys

"""
This solution is NOT generalized, in the sense that it does depend on the alphabet.
This solution uses the Counting Sort algorithm to sort the "bwt" into the first column.
Counting Sort is O(n), and needs a fixed and known alphabet in advance.
But, Tim Sort's O(n*log(n)) is not much slower than O(n).

The improvement that is applied in this solution is that it removes an entire O(n) loop, and
it replaces the Python standard library sorting function with my Counting Sort that doesn't only do
the sorting, but calculates necessary things at the same time, while performing the sorting.
So, this solution uses only one loop, which is O(n), where my other two solutions use
two loops - one for sorting, and the other for calculating "m" and "occurrences",
which is O(n). Sorting is O(n*log(n)) in case of Tim Sort, or O(n) in case of my Counting Sort.
So, the "preprocessing" phase in this solution is around twice as fast.

The matrix has len(bwt) rows and two columns.
The first column corresponds to sorted BWT, and the second column corresponds to the BWT.

Elements of the first column are tuples of characters and their increasing indices.
Elements of the second column are tuples of characters and their increasing indices.
The indices increase as characters repeat.

This is an implementation of the Last-to-First Property.
"""


# Alphabet should be defined in sorted order.
ALPHABET = ('$', 'A', 'C', 'G', 'T')


def _counting_sort(bwt):
    """Counting Sort

    This is the unmodified Counting Sort algorithm, but the function is modified so that it returns
    a desired matrix and "occurrences".
    """
    dim = len(bwt)

    m = [[("", 0) for w in range(2)] for h in range(dim)]  # list[tuple(str, int), tuple(str, int]; dim by 2
    occurrences = {}

    # An auxiliary dictionary that stores number of occurrences of each character.
    num_occurrences = {}

    count = {}
    position = {}
    for char in ALPHABET:
        num_occurrences[char] = 0
        count[char] = 0
        position[char] = 0

    for char in bwt:
        count[char] += 1
    # print(f"count = {count}")

    position['$'] = 0
    previous_char = ALPHABET[0]
    for j, char in enumerate(ALPHABET[1:], start=1):
        if count[char] > 0:
            position[char] = position[previous_char] + count[previous_char]
            previous_char = ALPHABET[j]
    # print(f"position = {position} [STARTING POSITIONS]")  # Starting positions at this point.

    for row, char in enumerate(bwt):
        npos = num_occurrences[char]
        num_occurrences[char] += 1
        occurrences[(char, npos)] = position[char]
        # print(f"row={row}, char={char}, pos[{char}]={position[char]}, npos={npos}, " +
        #       f"num_occ={num_occurrences}, occurrences={occurrences}")
        m[position[char]][0] = (char, npos)
        m[row][1] = (char, npos)
        position[char] += 1
    # print(f"num_occurrences = {num_occurrences}")
    # print(f"position = {position}")  # Ending positions at this point.
    # print(f"occurrences = {occurrences}")
    # print(f"m = {m}")

    return m, occurrences


def inverse_bwt(bwt):
    dim = len(bwt)
    result = [""] * dim

    m, occurrences = _counting_sort(bwt)

    current_letter = m[0][0]  # ('$', 0)
    row = occurrences[current_letter]
    for i in range(dim):
        # print(f"\ni = {i}: current_letter = {current_letter}, row = {row}")
        result[dim-1-i] = current_letter[0]
        next_letter = m[row][1]  # Same row.
        row = occurrences[next_letter]  # Row to which we jump to next.
        current_letter = m[row][0]  # We're in a new row now.
        # print(f"{i}: new current_letter={current_letter} next_letter={next_letter} row={row} result={''.join(result)}")

    return "".join(result)


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(inverse_bwt(bwt))
