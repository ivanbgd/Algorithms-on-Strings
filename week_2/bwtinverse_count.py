import sys

"""
This solution is NOT generalized, in the sense that it does depend on the alphabet.
This solution uses the Counting Sort algorithm to sort the "bwt" into the first column.
Counting Sort is O(n), and needs a fixed and known alphabet in advance.
But, Tim Sort's O(n*log(n)) is not much slower than O(n).

The matrix has len(bwt) rows and two columns.
The first column corresponds to sorted BWT, and the second column corresponds to the BWT.

Elements of the first column are tuples of characters and their increasing indices.
Elements of the second column are tuples of characters and their increasing indices.
The indices increase as characters repeat.

This is an implementation of the Last-to-First Property.
"""


ALPHABET = ('$', 'A', 'C', 'G', 'T')


def _counting_sort(bwt):
    dim = len(bwt)

    count = {}
    position = {}
    for char in ALPHABET:
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
    # print(f"position = {position}")

    sorted_bwt = [""] * dim
    for i, char in enumerate(bwt):
        sorted_bwt[position[char]] = char
        position[char] += 1

    sorted_bwt = "".join(sorted_bwt)
    # print(f"sorted_bwt = {sorted_bwt}")

    return sorted_bwt


def create_matrix(bwt):
    m = []
    occurrences = {}

    sorted_bwt = _counting_sort(bwt)

    # An auxiliary dictionary that stores number of occurrences of each character.
    num_occurrences = {}

    # A random letter that is not part of the alphabet.
    previous_letter = '#'

    cpos = 0
    for row, c in enumerate(sorted_bwt):
        current_letter = c
        next_letter = bwt[row]  # Same row.
        npos = num_occurrences.get(next_letter, 0)
        num_occurrences[next_letter] = npos + 1
        if current_letter == previous_letter:
            cpos += 1
        else:
            cpos = 0
            previous_letter = current_letter
        m.append([(current_letter, cpos), (next_letter, npos)])
        occurrences[(current_letter, cpos)] = row
        # print(row, ":", current_letter, cpos, ";", next_letter, npos)
    # print(f"{m}\n{occurrences}")
    return m, occurrences


def inverse_bwt(bwt):
    dim = len(bwt)
    result = [""] * dim

    m, occurrences = create_matrix(bwt)

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
