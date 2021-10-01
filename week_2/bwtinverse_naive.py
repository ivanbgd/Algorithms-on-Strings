import sys

# Correct, but slow.


def inverse_bwt(bwt):
    """Time: O(n**3 * log(n)); Space: O(n**2)

       We work with a "transpose" of a "matrix", but in which rows are in reversed order. It's easier this way.
       The "matrix" is really a list[str].
       If it were a list[list[str]], it would have occupied a lot more memory! But, there's no reason to use that.

       https://stackoverflow.com/questions/6667201/how-to-define-a-two-dimensional-array
       https://docs.python.org/3/faq/programming.html#faq-multidimensional-list
       `m = [[""] * dim for _ in range(dim)]`

       We can remove one dimension by: `m = ["" * dim for _ in range(dim)]`.
       But then, it's enough to just: `m = ["" for _ in range(dim)]`, or simply `m = [""] * dim`.
    """
    dim = len(bwt)
    result = [""] * dim
    m = [""] * dim
    # # for i in range(dim):  # Not transposed.
    # #     m[i][-1] = bwt[i]
    kmer = list(bwt)  # list[str]; k-mer; k increments in each iteration, and begins at 1
    column = "".join(kmer)
    # print(-1, kmer, column, "\n")
    m[0] = "".join(sorted(column))
    for i in range(1, dim):
        # print(i, m[i-1])
        # kmer = ["".join(t) for t in kmer]
        kmer = list(zip(kmer, m[i-1]))
        # kmer = ["".join(t) for t in kmer]
        sorted_kmer = sorted(kmer)
        column = "".join([t[-1] for t in sorted_kmer])
        m[i] = column
        result[i-1] = m[i][0]
        print(kmer, sorted_kmer, column, "\t", "".join(result))
        # print(m, "\n")
    # print(m, "\n\n")
    result[-1] = m[0][0]  # "$"
    return "".join(result)


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(inverse_bwt(bwt))
