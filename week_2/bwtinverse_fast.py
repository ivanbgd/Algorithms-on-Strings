import sys

"""
This solution is NOT generalized, in the sense that it does depend on the alphabet.
This solution uses the Counting Sort algorithm to sort the "bwt" into the first column.
Counting Sort is O(n), and needs a fixed and known alphabet in advance.
But, Tim Sort's O(n*log(n)) is not much slower than O(n).
Well, for n = 1000, it is 10 times slower, which is not little.

The improvement in this solution is that it removes the O(n) loop in the "inverse_bwt()" function.

The improvement that is applied in this solution is that it removes an entire O(n) loop, and
it replaces the Python standard library sorting function with my Counting Sort that doesn't only do
the sorting, but calculates necessary things at the same time, while performing the sorting.
So, this solution uses only one loop, which is O(n), where my other two solutions use
two loops - one for sorting, and the other for calculating "m" and "occurrences",
which is O(n). Sorting is O(n*log(n)) in case of Tim Sort, or O(n) in case of my Counting Sort.
So, the "preprocessing" phase in this solution is around twice as fast.

In this solution, we don't use the Last-to-First Property explicitly, but it is used implicitly.
http://web.stanford.edu/class/cs262/presentations/lecture4.pdf See slide 24/33. This is my "next_row".
We don't need the matrix.
We introduce the "bwt_with_ranks" list.
"""


# Alphabet should be defined in sorted order.
ALPHABET = ('$', 'A', 'C', 'G', 'T')


def counting_sort(bwt):
    """Counting Sort

    This is the unmodified Counting Sort algorithm, but the function is modified.
    """
    dim = len(bwt)

    bwt_with_ranks = [("", 0)] * dim

    count = {}
    position = {}
    for char in ALPHABET:
        count[char] = 0
        position[char] = 0

    for i, char in enumerate(bwt):
        bwt_with_ranks[i] = (char, count[char])
        count[char] += 1
    # print(f"bwt_with_ranks = {bwt_with_ranks}")
    # print(f"count = {count}")

    position['$'] = 0
    previous_char = ALPHABET[0]
    for j, char in enumerate(ALPHABET[1:], start=1):
        if count[char] > 0:
            position[char] = position[previous_char] + count[previous_char]
            previous_char = ALPHABET[j]
    # print(f"position = {position} [STARTING POSITIONS]")  # Starting positions at this point.

    next_row = 0
    current_letter = ('$', next_row)

    # result = [""] * dim
    # for row in range(dim):
    #     result[dim - 1 - row] = current_letter[0]
    #     next_letter = bwt_with_ranks[next_row]
    #     next_row = position[next_letter[0]] + next_letter[1]  # Row to which we jump to next.
    #     current_letter = next_letter  # We're in a new row now.

    # result = [""] * dim
    # for i in range(dim):
    #     result[i] = current_letter[0]
    #     next_letter = bwt_with_ranks[next_row]
    #     next_row = position[next_letter[0]] + next_letter[1]  # Row to which we jump to next.
    #     current_letter = next_letter  # We're in a new row now.
    # result.reverse()

    result = []
    for _ in range(dim):
        result.append(current_letter[0])
        next_letter = bwt_with_ranks[next_row]
        next_row = position[next_letter[0]] + next_letter[1]  # Row to which we jump to next.
        current_letter = next_letter  # We're in a new row now.
    result.reverse()

    return "".join(result)


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(counting_sort(bwt))
