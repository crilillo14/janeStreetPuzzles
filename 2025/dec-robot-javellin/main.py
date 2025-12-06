import seaborn as sbn
import numpy as np
import scipy as sp
import polars as pl

"""Resolves the final Spears Robot distance. Cheater"""

"""d > 1/2"""


def resolveS_a(d: float, s1: float, bit: bool):
    s2 = np.random.uniform(0, 1)
    # trivial cases:


"""d < 1/2"""


def resolveS_b(d: float, s1: float, bit: bool):
    s2 = np.random.uniform(0, 1)

    if bit:
        if s1 < d:
            return s2
        else:
            pass
    else:
        if s1 < d:
            k = 1 - s1
            l = 2*k
            return s2 if d < l - np.sqrt(l * (l - 1)) else s1
        else:
            pass


"""
One trial given some d. d is used for checking j1 < d.
No need to do anything fancy for > d, uniformity and iid imply d = 1-d* at the end.

"""


def trial(d: float):
    seed = 1000 * int(np.random())
    np.random.seed(seed)

    ts = 0
    tj = 0

    # javellin throw
    j1 = np.random.uniform(0, 1)
    s1 = np.random.uniform(0, 1)

    tj = np.random.uniform(0, 1) if j1 < 0.5 else j1

    bit = j1 < d
    if d > 0.5:
        ts = resolveS_a(d, s1, bit)
    else:
        ts = resolveS_b(d, s1, bit)

    return ts > tj


def main():
    "idea: Asking j1 < d should be maximally informative for Spears, thus should be "


if __name__ == "__main__":
    main()
