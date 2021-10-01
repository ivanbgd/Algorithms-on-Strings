import sys

"""
This solution is generalized, in the sense that it doesn't depend on the alphabet. It works with any alphabet.

This solution uses the Python standard library Tim Sort algorithm for sorting, which is O(n*log(n)).

The matrix has len(bwt) rows and two columns.
The first column corresponds to sorted BWT, and the second column corresponds to the BWT.

Elements of the first column are tuples of characters and their increasing indices.
Elements of the second column are tuples of characters and their increasing indices.
The indices increase as characters repeat.

This is an implementation of the Last-to-First Property.
"""


def create_matrix(bwt):
    m = []
    occurrences = {}

    sorted_bwt = sorted(bwt)

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
