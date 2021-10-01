""" Test and compare various implementations to one another """
from datetime import timedelta
from random import choices
from timeit import default_timer as timer

import suffix_array_naive
import suffix_array_heapq
import suffix_array_stree
import suffix_array_stree_timer


"""
Naive and HeapQ are roughly the same speed. They both crash when LENGTH = 10**5, due to memory.
They crashed the IDE.
They can handle LENGTH = 2 * 10**4.

The Suffix Tree variant is multiple times faster than Naive and HeapQ.
I have only tested it with LENGTH = 2 * 10**4, not higher.

I tried with `text = ['A'] * 1000`, `text[-1] = '$'`, and got:
Naive took 0.015704100000000012 s [0:00:00.015704]
HeapQ took 0.03784089999999998 s [0:00:00.037841]
STree took 0.17892829999999998 s [0:00:00.178928]
So, this seems to be the anomaly I had in mind, but it's still way less than a second, on my computer.
If I repeat "AC" for 500 times, or "ACGT" for 250 times, STree wil be slower again.
So, I guess STree doesn't like long runs or repeats.
"""


ALPHABET = ('A', 'C', 'G', 'T')
LENGTH = 2 * 10**4


def generate_text(length):
    start = timer()
    text = choices(population=ALPHABET, k=length)
    text[-1] = '$'
    end = timer()
    execution_time = end - start
    print(f"Generating text took {execution_time} s [{timedelta(seconds=execution_time)}].\n")  # Real fast.
    return text


def compare(text):
    start = timer()
    naive = suffix_array_naive.build_suffix_array(text)
    end = timer()
    execution_time = end - start
    print(f"Naive took {execution_time} s [{timedelta(seconds=execution_time)}]")
    # print(f"Naive: {naive}")

    start = timer()
    heap = suffix_array_heapq.build_suffix_array(text)
    end = timer()
    execution_time = end - start
    print(f"HeapQ took {execution_time} s [{timedelta(seconds=execution_time)}]")
    # print(f"HeapQ: {heap}")

    start = timer()
    suffix_tree = suffix_array_stree.build_suffix_array(text)
    end = timer()
    execution_time = end - start
    print(f"STree took {execution_time} s [{timedelta(seconds=execution_time)}]")
    # print(f"STree: {suffix_tree}")

    start = timer()
    suffix_tree = suffix_array_stree_timer.build_suffix_array(text)
    end = timer()
    execution_time = end - start
    print(f"STree took {execution_time} s [{timedelta(seconds=execution_time)}]")
    # print(f"STree: {suffix_tree}")

    assert naive == heap  # Real fast.
    assert naive == suffix_tree  # Real fast.


if __name__ == '__main__':
    text = generate_text(LENGTH)
    # print(f"Text: {text}\n")
    compare(text)
