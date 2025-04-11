

import mpmath as mp
from scipy.optimize import brentq

# Set desired precision
mp.dps = 100  # increase if needed

def f(x_float, n):
    x = mp.mpf(x_float)
    base = 1 - n * x**n - n * x**(n+1) - x**n
    value = base**(2**n) - mp.mpf(0.5)
    return float(value)

# For example, try a large n
n = 80

# Find the root between two points; use your intuition from Desmos
x_left = 0.0
x_right = 1.0

root = brentq(f, x_left + 1e-10, x_right - 1e-10, args=(n,))
print(f"The intercept x for n={n} is approximately: {root}")