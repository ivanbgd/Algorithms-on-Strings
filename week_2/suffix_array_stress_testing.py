""" Stress testing the Suffix Tree variant

    The idea is to find the corner case that makes the Suffix Tree work abnormally slowly - an anomaly.
"""

import random
from datetime import timedelta
from random import choices
from timeit import default_timer as timer

import suffix_array_naive
import suffix_array_stree

MAX_TIME = 0.3

ALPHABET = ('A', 'C', 'G', 'T')
MAX_LENGTH = 10**4


def generate_text(length):
    text = choices(population=ALPHABET, k=length)
    text[-1] = '$'
    return text


def compare(text):
    start = timer()
    naive = suffix_array_naive.build_suffix_array(text)
    end = timer()
    naive_time = end - start

    start = timer()
    suffix_tree = suffix_array_stree.build_suffix_array(text)
    end = timer()
    stree_time = end - start

    if naive != suffix_tree or (stree_time >= naive_time and stree_time > MAX_TIME):
        print(f"\a\nText: {text}")
        print(f"Text: {''.join(text)}")
        print(f"Length of text: {len(text)}")
        print(f"Naive took {naive_time:.6f} s [{timedelta(seconds=naive_time)}]")
        print(f"STree took {stree_time:.6f} s [{timedelta(seconds=stree_time)}]")
        print(f"Naive: {naive}")
        print(f"STree: {suffix_tree}")
        print(f"Differences: {set(naive) ^ set(suffix_tree)}")
        if stree_time > MAX_TIME:
            print(f"Time limit of {MAX_TIME} s for Suffix Tree broken! STree took {stree_time:.3f} s.")
        return False
    else:
        print(f"Naive time = {naive_time:.3f} s, STree time = {stree_time:.3f} s,", end=' ')
        return True


def loop():
    start = timer()
    i = 0
    okay = True
    while okay:
        length = random.randint(1, MAX_LENGTH)
        text = generate_text(length)
        print(f"i = {i:6}: length = {length:5},", end=' ')
        okay = compare(text)
        print(f"okay = {okay}")
        i += 1
    end = timer()
    total_time = end - start
    print(f"\nTotal time: {total_time} s [{timedelta(seconds=total_time)}]")


if __name__ == '__main__':
    loop()
