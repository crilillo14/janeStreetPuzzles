import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def compute_p_fixed_point(n, max_iterations=100, tolerance=1e-10, initial_guess=0.5):
    """
    Compute p for a given n using fixed-point iteration
    
    Args:
        n: The parameter n in the equation
        max_iterations: Maximum number of iterations
        tolerance: Convergence tolerance
        initial_guess: Initial guess for p
    
    Returns:
        Computed value of p
    """
    # Define K
    K = (1/2)**(1/(2**n))
    
    # Define the fixed-point function: p = g(p)
    def g(p):
        return ((1 - K) / (1 + n * (1 + p)))**(1/n)
    
    p_current = initial_guess
    for i in range(max_iterations):
        p_next = g(p_current)
        if abs(p_next - p_current) < tolerance:
            return p_next, i+1  # Return solution and iteration count
        p_current = p_next
    
    # If we reached max iterations without converging
    print(f"Warning: Fixed-point iteration did not converge after {max_iterations} iterations")
    return p_current, max_iterations

def compute_p_newton(n, max_iterations=100, tolerance=1e-10, initial_guess=0.5):
    """
    Compute p for a given n using Newton's method
    
    Args:
        n: The parameter n in the equation
        max_iterations: Maximum number of iterations
        tolerance: Convergence tolerance
        initial_guess: Initial guess for p
    
    Returns:
        Computed value of p
    """
    # Define K
    K = (1/2)**(1/(2**n))
    
    # Define the function f(p) = 0 and its derivative
    def f(p):
        return (1 - n*(p**n) - n*p**(n+1) - p**n) - K
    
    def f_prime(p):
        return -n**2 * p**(n-1) - n*(n+1)*p**n - n*p**(n-1)
    
    p_current = initial_guess
    for i in range(max_iterations):
        f_value = f(p_current)
        f_prime_value = f_prime(p_current)
        
        if abs(f_prime_value) < 1e-10:  # Avoid division by near-zero
            print("Warning: Derivative close to zero")
            break
            
        p_next = p_current - f_value / f_prime_value
        
        if abs(p_next - p_current) < tolerance:
            return p_next, i+1  # Return solution and iteration count
        
        p_current = p_next
    
    # If we reached max iterations without converging
    print(f"Warning: Newton's method did not converge after {max_iterations} iterations")
    return p_current, max_iterations

def compute_p_scipy(n):
    """
    Compute p for a given n using SciPy's fsolve
    
    Args:
        n: The parameter n in the equation
    
    Returns:
        Computed value of p
    """
    # Define K
    K = (1/2)**(1/(2**n))
    
    # Define the function where f(p) = 0
    def f(p):
        return (1 - n*(p**n) - n*p**(n+1) - p**n) - K
    
    # Use SciPy's fsolve with initial guess of 0.5
    result = fsolve(f, 0.5)
    return result[0]

def verify_solution(n, p):
    """
    Verify if p is a solution for the given n
    
    Args:
        n: The parameter n
        p: The computed value of p
    
    Returns:
        The value of the original equation, should be close to 0.5
    """
    result = (1 - n*(p**n) - n*p**(n+1) - p**n)**(2**n)
    return result

# Example usage
def main():
    # Test with several values of n
    n_values = [1, 2, 3, 4, 5, 10, 20]
    
    print(f"{'n':<5} {'p (Fixed-Point)':<20} {'p (Newton)':<20} {'p (SciPy)':<20} {'Verification':<15}")
    print("-" * 80)
    
    results = []
    
    for n in n_values:
        # Compute p using different methods
        p_fixed, iters_fixed = compute_p_fixed_point(n)
        p_newton, iters_newton = compute_p_newton(n)
        p_scipy = compute_p_scipy(n)
        
        # Verify the solutions
        verify_fixed = verify_solution(n, p_fixed)
        verify_newton = verify_solution(n, p_newton)
        verify_scipy = verify_solution(n, p_scipy)
        
        # Print results
        print(f"{n:<5} {p_fixed:<20.16f} {p_newton:<20.16f} {p_scipy:<20.16f} {verify_scipy:<15.12f}")
        
        results.append((n, p_scipy))
    
    # Plot the relationship between n and p
    ns, ps = zip(*results)
    plt.figure(figsize=(10, 6))
    plt.plot(ns, ps, 'o-', label='p vs n')
    plt.xlabel('n')
    plt.ylabel('p')
    plt.title('Relationship between p and n')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()