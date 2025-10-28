import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from mpmath import mp, power, mpf
import warnings

# Set precision for mpmath
mp.dps = 50  # 50 digits of precision

def compute_p_scipy_stable(n, initial_guess=0.5):
    """
    Compute p for a given n using SciPy's fsolve with log-transformed equations
    for numerical stability with large n values
    
    Args:
        n: The parameter n in the equation
        initial_guess: Initial guess for p
    
    Returns:
        Computed value of p
    """
    # For large n, we need to be careful with how we compute K = (1/2)^(1/2^n)
    # For large n, 1/2^n becomes very small, and K approaches 1
    
    # Define a numerically stable function
    def f(p):
        # For large n, working with logs is more stable
        if n > 30:
            # For large n, log(K) ≈ -log(2)/2^n which is very close to 0
            # This means K is very close to 1, so 1-K is very small
            log_K = -np.log(2) / (2**n)
            # K ≈ 1 + log_K for small log_K (first-order Taylor approximation)
            K = 1 + log_K
            
            # For large n, the original equation approaches:
            # p^n(1 + n(1 + p)) ≈ 1 - K ≈ -log_K ≈ log(2)/2^n
            # So we can check if p satisfies this relationship
            lhs = p**n * (1 + n*(1 + p))
            rhs = -log_K
            return lhs - rhs
        else:
            # Original approach for smaller n
            K = (1/2)**(1/(2**n))
            return (1 - n*(p**n) - n*p**(n+1) - p**n) - K
    
    # Use SciPy's fsolve
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = fsolve(f, initial_guess)
    
    return result[0]

def compute_p_mpmath(n, initial_guess=0.5, max_iterations=100, tolerance=1e-20):
    """
    Compute p for a given n using mpmath for arbitrary precision
    
    Args:
        n: The parameter n in the equation
        initial_guess: Initial guess for p
        max_iterations: Maximum number of iterations
        tolerance: Convergence tolerance
    
    Returns:
        Computed value of p
    """
    n = mpf(n)
    p = mpf(initial_guess)
    
    # For very large n, we use an approximation
    if n > 100:
        # For large n, p approaches (log(2)/n)^(1/n)
        # This is because as n gets very large, the equation simplifies
        return float(power(mp.log(2)/n, 1/n))
    
    # For more moderate n, use Newton's method with mpmath
    for i in range(max_iterations):
        # Define K
        K = power(mpf(0.5), 1/power(2, n))
        
        # Calculate f(p) and f'(p)
        f_p = (1 - n*power(p, n) - n*power(p, n+1) - power(p, n)) - K
        fp_p = -n*n*power(p, n-1) - n*(n+1)*power(p, n) - n*power(p, n-1)
        
        # Newton step
        p_next = p - f_p/fp_p
        
        # Check convergence
        if abs(p_next - p) < tolerance:
            return float(p_next)
        
        p = p_next
    
    # If didn't converge
    print(f"Warning: Newton's method with mpmath did not converge after {max_iterations} iterations")
    return float(p)

def get_asymptotic_approximation(n):
    """
    Get asymptotic approximation for p when n is large
    
    Args:
        n: The parameter n in the equation
    
    Returns:
        Approximate value of p
    """
    # For large n, p approaches (log(2)/n)^(1/n)
    return (np.log(2)/n)**(1/n)

def verify_solution(n, p):
    """
    Verify if p is a solution for the given n
    
    Args:
        n: The parameter n
        p: The computed value of p
    
    Returns:
        The value of the original equation, should be close to 0.5
    """
    # For large n, use mpmath for verification
    if n > 30:
        n_mp = mpf(n)
        p_mp = mpf(p)
        result = power(1 - n_mp*power(p_mp, n_mp) - n_mp*power(p_mp, n_mp+1) - power(p_mp, n_mp), power(2, n_mp))
        return float(result)
    else:
        # Use numpy for smaller n
        return float((1 - n*(p**n) - n*p**(n+1) - p**n)**(2**n))

def main():
    # Test with a range of n values including large ones
    small_n_values = [1, 2, 3, 4, 5, 10, 20, 30]
    large_n_values = [50, 100, 200, 500, 1000]
    
    results_small = []
    results_large = []
    results_asymptotic = []
    
    print("Computing for small n values...")
    print(f"{'n':<5} {'p (SciPy)':<25} {'p (mpmath)':<25} {'Verification':<15}")
    print("-" * 70)
    
    for n in small_n_values:
        p_scipy = compute_p_scipy_stable(n)
        p_mpmath = compute_p_mpmath(n)
        
        # Verify the solution (use mpmath for verification)
        verify = verify_solution(n, p_mpmath)
        
        print(f"{n:<5} {p_scipy:<25.16f} {p_mpmath:<25.16f} {verify:<15.10f}")
        results_small.append((n, p_mpmath))
    
    print("\nComputing for large n values...")
    print(f"{'n':<7} {'p (mpmath)':<25} {'p (asymptotic)':<25} {'Difference':<15}")
    print("-" * 70)
    
    for n in large_n_values:
        # Use mpmath for large n
        p_mpmath = compute_p_mpmath(n)
        
        # Also calculate asymptotic approximation
        p_asymptotic = get_asymptotic_approximation(n)
        
        difference = abs(p_mpmath - p_asymptotic)
        
        print(f"{n:<7} {p_mpmath:<25.16f} {p_asymptotic:<25.16f} {difference:<15.10e}")
        results_large.append((n, p_mpmath))
        results_asymptotic.append((n, p_asymptotic))
    
    # Plot the results
    plt.figure(figsize=(12, 8))
    
    # Plot small n values
    ns_small, ps_small = zip(*results_small)
    plt.subplot(2, 1, 1)
    plt.plot(ns_small, ps_small, 'o-', label='p vs n (small n)')
    plt.xlabel('n')
    plt.ylabel('p')
    plt.title('Relationship between p and n (small n values)')
    plt.grid(True)
    plt.legend()
    
    # Plot large n values and asymptotic approximation
    if results_large:
        ns_large, ps_large = zip(*results_large)
        ns_asymptotic, ps_asymptotic = zip(*results_asymptotic)
        
        plt.subplot(2, 1, 2)
        plt.plot(ns_large, ps_large, 'o-', label='p vs n (large n)')
        plt.plot(ns_asymptotic, ps_asymptotic, 's--', label='Asymptotic approximation')
        plt.xlabel('n')
        plt.ylabel('p')
        plt.title('Relationship between p and n (large n values)')
        plt.grid(True)
        plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Also print the asymptotic formula
    print("\nAsymptotic formula for large n:")
    print("p ≈ (log(2)/n)^(1/n)")

if __name__ == "__main__":
    main()