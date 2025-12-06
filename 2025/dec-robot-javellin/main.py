import seaborn as sns
import numpy as np
from scipy.optimize import minimize_scalar

import os
import polars as pl
import matplotlib.pyplot as plt

iterations = 0

"""d < 1/2 implied. Solves S's preference of S1 or S2."""
def resolveS(d: float, s1: float, bit: bool, s2: float, N: int):

    if bit:
        if s1 < d:
            return s2
        else:
            return s1
    else:
        if s1 < d:
            return s2
        else:
            return s2 if (0.5*s1 - 0.25) / (s1 - 0.75) < d else s1


def resolveS_mask(d: float, s1: np.ndarray, bit: np.ndarray) -> np.ndarray:
    # base condition
    cond1 = s1 < d

    # compute r = (0.5*s1 - 0.25) / (s1 - 0.75), safely
    den = s1 - 0.75
    with np.errstate(divide='ignore', invalid='ignore'):
        r = (0.5 * s1 - 0.25) / den
    r = np.where(den == 0.0, np.inf, r)  # avoid NaNs at s1==0.75

    # when bit==True -> select s2 iff s1<d
    # when bit==False -> select s2 if s1<d, else select s2 iff r<d
    select_s2 = np.where(bit, cond1, cond1 | ((~cond1) & (r < d)))
    return select_s2

def save_epoch_plots(d: float, spears_win: np.ndarray, bit: np.ndarray, iteration : int, out_dir: str = "figures"):
    """
    Save a figure with 3 lines across sample index:
    - d (constant line)
    - cumulative winrate (cumulative mean of spears_win)
    - cumulative information gained (cumulative mean of bit = [j1 < d])
    """
    N = spears_win.shape[0]
    idx = np.arange(1, N + 1)
    cum_winrate = np.cumsum(spears_win) / idx
    cum_info = np.cumsum(bit) / idx
    d_line = np.full(N, d)

    os.makedirs(out_dir, exist_ok=True)
    fname = f"iter_{iteration}.png"
    path = os.path.join(out_dir, fname)

    # Build tidy DataFrame for relplot (use Polars, then convert to pandas for seaborn)
    df = pl.DataFrame({
        "iteration": np.concatenate([idx, idx, idx]),
        "value": np.concatenate([d_line, cum_winrate, cum_info]),
        "metric": np.repeat(["d", "cumulative winrate", "information gained (P[j1 < d])"], repeats=N),
    }).to_pandas()

    sns.set_theme(style="ticks")
    g = sns.relplot(
        data=df,
        x="iteration", y="value",
        hue="metric",
        kind="line",
        height=5, aspect=1.6,
        palette="rocket_r",
        facet_kws=dict(legend_out=False),
    )
    g.set_axis_labels("iteration (sample index)", "value")
    # Put title inside the single facet axes instead of a suptitle
    g.ax.set_title(f"Trial metrics (d={d:.6f}, N={N})")
    # Keep legend inside and stable
    if g._legend is not None:
        g._legend.set_title(None)
        g._legend.set_loc("best")
    g.figure.tight_layout()
    g.figure.savefig(path, dpi=160)
    g.figure.clear()
    plt.close(g.figure)
    



"""
One trial given some d. d is used for checking j1 < d.
No need to do anything fancy for > d, uniformity and iid imply d = 1-d* at the end.

"""
def trial(d: float, N):
    global iterations
    
    iterations += 1
    np.random.seed()

    ts = np.zeros(N)
    tj = np.zeros(N)

    # javellin throw
    j1 = np.random.uniform(0, 1, N)
    s1 = np.random.uniform(0, 1, N)
    j2 = np.random.uniform(0, 1, N)

    mask = j1 > 0.5

    tj = np.where(mask, j1, j2)

    bit = j1 < d
    information_gained = sum(bit) / N

    s2 = np.random.uniform(0, 1, size=N)
    ts = np.where(resolveS_mask(d, s1, bit), s2, s1)

    spears_win = ts > tj
    # wins = np.where(spears_win, ts, tj)

    # save plot with 3 lines for this trial
    save_epoch_plots(d, spears_win.astype(int), bit.astype(int), iterations, out_dir="figures")

    return sum(spears_win) / N, information_gained


def objective(d):
    winrate, _ = trial(d, 10000)
    return -winrate


def run():
    result = minimize_scalar(objective, bounds=(
        0.00, 0.50), method='bounded', options={'xatol': 1e-12})

    maximally_informative_d = result.x
    max_winrate = -result.fun

    print(f"Maximum winrate achieved : {max_winrate:.10f}")
    print(f"Maximally Informative d boundary: {maximally_informative_d:.10f}")
    
    return maximally_informative_d, max_winrate 

def main():
    "idea: Asking j1 < d should be maximally informative for Spears, thus should be 50%"
    for i in range(10):
        run()


if __name__ == "__main__":
    main()
