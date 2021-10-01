import sys


def compute_prefix_function(text):
    dim = len(text)
    prefix = [0] * dim
    border = 0
    for i in range(1, dim):
        while border > 0 and text[i] != text[border]:
            border = prefix[border-1]
        if text[i] == text[border]:
            border += 1
        else:
            border = 0
        prefix[i] = border
    return prefix


def find_pattern(pattern, text):
    """
    Find all the occurrences of the pattern in the text
    and return a list of all positions in the text
    where the pattern starts in the text.
    """
    result = []
    merged = pattern + '$' + text
    prefix = compute_prefix_function(merged)
    pattern_length = len(pattern)
    for i in range(pattern_length+1, len(merged)):
        if prefix[i] == pattern_length:
            result.append(i - 2*pattern_length)
    return result


if __name__ == '__main__':
    pattern = sys.stdin.readline().strip()
    text = sys.stdin.readline().strip()
    result = find_pattern(pattern, text)
    print(" ".join(map(str, result)))
