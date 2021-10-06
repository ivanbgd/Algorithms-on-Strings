import sys

"""
In this solution, we use the fast algorithm for creating suffix array of a string from this week's
"suffix_array_long.py", and create the string's BWT from its suffix array.
http://web.stanford.edu/class/cs262/presentations/lecture4.pdf (slide 16/33)
We need to rotate left by one position to get a BWT from a SA.

Then, we use the BWT multiple matching algorithm from Week's 2 "bwtmatching_13.py".

We expect this solution to be slower than the original solution, "suffix_array_matching.py",
which uses two binary searches to find starting and ending position of a pattern in a
suffix array of a text. This solution is simply an exercise, nothing more.
Well, it has the same speed, apparently, and just a tiny bit higher memory consumption.
"""


ALPHABET = {
    '$': 0,
    'A': 1,
    'C': 2,
    'G': 3,
    'T': 4,
}


def sort_characters(text, alphabet):
    """Counting Sort"""
    dim = len(text)
    order = [0] * dim
    count = {k: 0 for v, k in enumerate(alphabet)}

    for char in text:
        count[char] += 1

    for j in range(1, len(alphabet)):
        count[alphabet[j]] += count[alphabet[j-1]]

    for i, char in reversed(tuple(enumerate(text))):
        count[char] -= 1
        order[count[char]] = i
    return order


def compute_char_classes(text, order):
    dim = len(text)
    klass = [0] * dim
    for i in range(1, dim):
        if text[order[i]] != text[order[i-1]]:
            klass[order[i]] = klass[order[i-1]] + 1
        else:
            klass[order[i]] = klass[order[i-1]]
    return klass


def sort_doubled(text, length, order, klass):
    dim = len(text)
    count = [0] * dim
    new_order = [0] * dim

    for i in range(dim):
        count[klass[i]] += 1
    for j in range(1, dim):
        count[j] += count[j-1]
    for i in range(dim-1, -1, -1):
        start = (order[i] - length + dim) % dim
        kl = klass[start]
        count[kl] -= 1
        new_order[count[kl]] = start
    return new_order


def update_classes(new_order, klass, length):
    n = len(new_order)
    new_class = [0] * n
    for i in range(1, n):
        current = new_order[i]
        previous = new_order[i-1]
        middle = (current + length) % n
        mid_prev = (previous + length) % n
        if klass[current] != klass[previous] or klass[middle] != klass[mid_prev]:
            new_class[current] = new_class[previous] + 1
        else:
            new_class[current] = new_class[previous]
    return new_class


def build_suffix_array(text, alphabet):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    order = sort_characters(text, alphabet)
    klass = compute_char_classes(text, order)
    length = 1
    while length < len(text):
        order = sort_doubled(text, length, order, klass)
        klass = update_classes(order, klass, length)
        length *= 2
    return order


def bwt_from_suffix_array(text, suffix_array):
    bwt = [text[pos - 1] for pos in suffix_array]
    return "".join(bwt)


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

    for char in ALPHABET:
        starts[char] = 0
    for i, char in enumerate(sorted_bwt):
        if starts[char] == 0:
            starts[char] = i

    for alpha in ALPHABET:
        counter = 0
        count = [counter]
        for char in bwt:
            if char == alpha:
                counter += 1
            count.append(counter)
        occ_counts_before[alpha] = count

    # print(f"starts = {starts}")
    # print(f"occ_counts_before = {occ_counts_before}")
    return starts, occ_counts_before


def return_occurrences(pattern, bwt, starts, occ_counts_before):
    """
    Find occurrences of a string pattern in a text,
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
            top = starts[symbol] + occ_counts_before[symbol][top]
            bottom = starts[symbol] + occ_counts_before[symbol][bottom + 1] - 1
            # print(f"top = {top}, bottom = {bottom}")
        else:
            # print(f"--> EMPTY. bottom = {bottom}, top = {top}\n")
            return top, bottom + 1
        i -= 1

    # print(f"--> NO OCCURRENCE of pattern '{pattern}'.\n")
    return None


def find_occurrences(text, patterns, alphabet):
    occurrences = set()

    suffix_array = build_suffix_array(text, alphabet)
    bwt = bwt_from_suffix_array(text, suffix_array)
    # print(f"suffix_array: {suffix_array}")
    # print(f"BWT: {bwt}")

    # Preprocess the BWT once, to get starts and occ_counts_before.
    # For each pattern, we will then use these precomputed values and
    # spend only O(|pattern|) to find all occurrences of the pattern
    # in the text instead of O(|pattern| + |text|).
    starts, occ_counts_before = preprocess_bwt(bwt)

    for pattern in patterns:
        result = return_occurrences(pattern, bwt, starts, occ_counts_before)
        if result is not None:
            start, end = result
            for i in range(start, end):
                pos = suffix_array[i]
                occurrences.add(pos)

    return occurrences


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()

    text += '$'
    alphabet = sorted(set(text))
    # alphabet = [key for key in ALPHABET.keys()]
    # alphabet = ('$', 'A', 'C', 'G', 'T')  # 'Cuz Python 3.4 :roll_eyes: ...
    # print(alphabet)

    occs = find_occurrences(text, patterns, alphabet)

    print(" ".join(map(str, occs)))
