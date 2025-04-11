import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e

# Define the function
def p(n):
    return 2 * np.exp(-1 / ((n - 1) * 2 ** n))

# Generate large n values
n_vals = np.arange(10, 200, 1)
p_vals = p(n_vals)

# Print the last value as n → ∞ approx
print(f"Approximation of p(n) as n→∞: {p_vals[-1]}")

# Plotting
plt.plot(n_vals, p_vals)
plt.title('Behavior of p(n) as n → ∞')
plt.xlabel('n')
plt.ylabel('p(n)')
plt.grid(True)
plt.show()
