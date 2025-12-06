import seaborn as sbn
import numpy as np
import scipy as sp
import polars as pl

"""Resolves the final Spears Robot distance. Cheater"""


def resolveS(d: float, t1j: float, t1s: float):

    # trivial cases:

    bit = t1j < d

    # 8 cases:


"""
One trial given some d. d is used for checking t1j < d.
No need to do anything fancy for > d, uniformity and iid imply d = 1-d* at the end.

"""

def trial(d: float, size : int = 1):
    seed = 1000 * int(np.random())
    np.random.seed(seed)

    ts = 0
    tj = 0

    # javellin throw
    t1j = np.random.uniform(0, 1)
    t1s = np.random.uniform(0, 1)

    tj = np.random.uniform(0, 1) if t1j < 0.5 else t1j

    if d > 0.5:
        ts = resolveS_a(d, t1j, t1s)
    else:
        ts = resolveS_b(d, t1j, t1s)

    return


def main():
    "idea: Asking t1j < d should be maximally informative for Spears, thus should be "

if __name__ == "__main__":
    main()
