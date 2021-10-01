import sys


def cyclic_rotations(text):
    cyclic = []
    for i in range(len(text)):
        rotation = text[i:] + text[:i]
        cyclic.append(rotation)
    return cyclic


def sorted_rotations(cyclic):
    cyclic.sort()
    return cyclic


def extract_last_column(matrix):
    last = []
    for _, row in enumerate(matrix):
        last.append(row[-1])
    return "".join(last)


def bwt(text):
    cyclic = cyclic_rotations(text)
    sorted_ = sorted_rotations(cyclic)
    last_column = extract_last_column(sorted_)
    return last_column


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(bwt(text))
