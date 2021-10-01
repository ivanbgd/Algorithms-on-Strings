import sys
import numpy as np

# Slow.

"""
This solution is generalized, in the sense that it doesn't depend on the alphabet. It works with any alphabet.

The matrix has len(bwt) rows and two columns.
The first column corresponds to sorted BWT, and the second column corresponds to the BWT.

Elements of the first column are tuples of characters and their increasing indices.
Elements of the second column are tuples of characters and their increasing indices.
The indices increase as characters repeat.
"""


def create_matrix(bwt):
    dim = len(bwt)
    m = np.recarray(shape=(dim, 2), dtype=[("char", "S1"), ("pos", "int")])
    occurrences = {}

    sorted_bwt = sorted(bwt)

    # An auxiliary dictionary that stores number of occurrences of each character.
    num_occurrences = {}

    previous_letter = '#'
    cpos = 0
    for row, c in enumerate(sorted_bwt):
        current_letter = c
        next_letter = bwt[row]
        npos = num_occurrences.get(next_letter, 0)
        num_occurrences[next_letter] = npos + 1
        if current_letter == previous_letter:
            cpos += 1
        else:
            cpos = 0
            previous_letter = current_letter
        m[row] = [(current_letter, cpos), (next_letter, npos)]
        occurrences[(current_letter, cpos)] = row
        # print(row, ":", current_letter, cpos, ";", next_letter, npos)
    # print(f"{m}\n{occurrences}")
    m.flags.writeable = False  # Needed, to be able to hash a Numpy array - to make it read-only, i.e., immutable.
    return m, occurrences


def inverse_bwt(bwt):
    dim = len(bwt)
    result = [""] * dim

    m, occurrences = create_matrix(bwt)

    current_letter = m[0][0]  # (b'$', 0); dtype is: (numpy.record, [('char', 'S1'), ('pos', '<i4')]); type is: <class 'numpy.record'>
    cur_let_unicode = current_letter.char.decode("ascii")
    row = occurrences[(cur_let_unicode, current_letter.pos)]
    for i in range(dim):
        # print(f"\ni = {i}: current_letter = {current_letter}, row = {row}")
        result[dim-1-i] = cur_let_unicode
        next_letter = m[row][1]
        row = occurrences[(next_letter.char.decode("ascii"), next_letter.pos)]
        current_letter = m[row][0]
        cur_let_unicode = current_letter.char.decode("ascii")
        # print(f"{i}: new current_letter={current_letter} next_letter={next_letter} row={row} result={''.join(result)}")

    return "".join(result)


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(inverse_bwt(bwt))
