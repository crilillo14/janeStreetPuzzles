
import mpmath as mp
from scipy.optimize import brentq

mp.dps = 100

def f(p_float, n):
    p = mp.mpf(p_float)
    base = 1 - n * p**n - n * p**(n+1) - p**n
    return float(base**(2**n) - mp.mpf(0.5))

n = 80

# Try values around your heuristic p ~ 0.929248
search_range = (0.91, 0.94)
step = 0.0005

# Scan for a sign change
a, b = None, None
x = search_range[0]
while x < search_range[1]:
    f1 = f(x, n)
    f2 = f(x + step, n)
    if f1 * f2 < 0:
        a, b = x, x + step
        break
    x += step

if a is not None and b is not None:
    root = brentq(f, a, b, args=(n,))
    print(f"Estimated p for n={n} is about: {root}")
else:
    print("Couldn't find a sign change in the given interval.")
