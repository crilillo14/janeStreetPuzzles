import numpy as np
from mpmath import mp, mpf, power, nstr
import pandas as pd

# Set precision for mpmath - this will ensure 10+ decimal places
mp.dps = 50  # 50 digits of precision should be more than enough

def compute_p_high_precision(n, max_iterations=100, tolerance=1e-20, initial_guess=None):
    """
    Compute p for a given n with high precision using mpmath
    
    Args:
        n: The parameter n in the equation
        max_iterations: Maximum number of iterations
        tolerance: Convergence tolerance
        initial_guess: Initial guess for p (default is asymptotic approximation)
    
    Returns:
        Computed value of p with high precision
    """
    n = mpf(n)
    
    # For initial guess, use asymptotic approximation if not provided
    if initial_guess is None:
        if n > 20:
            # For large n, use asymptotic approximation as initial guess
            initial_guess = power(mp.log(2)/n, 1/n)
        else:
            # For smaller n, 0.5 is a reasonable starting point
            initial_guess = mpf(0.5)
    
    p = mpf(initial_guess)
    
    # Use Newton's method with mpmath for high precision
    for i in range(max_iterations):
        # Define K = (1/2)^(1/2^n)
        K = power(mpf(0.5), 1/power(2, n))
        
        # Calculate f(p) and f'(p)
        f_p = (1 - n*power(p, n) - n*power(p, n+1) - power(p, n)) - K
        fp_p = -n*n*power(p, n-1) - n*(n+1)*power(p, n) - n*power(p, n-1)
        
        # Newton step
        delta = f_p/fp_p
        p_next = p - delta
        
        # Check convergence
        if abs(delta) < tolerance:
            # Verify the solution
            verification = verify_solution_high_precision(n, p_next)
            return p_next, verification, i+1
        
        p = p_next
    
    # If didn't converge, return best estimate
    verification = verify_solution_high_precision(n, p)
    return p, verification, max_iterations

def verify_solution_high_precision(n, p):
    """
    Verify if p is a solution for the given n with high precision
    
    Args:
        n: The parameter n
        p: The computed value of p
    
    Returns:
        The value of the original equation, should be close to 0.5
    """
    # Use mpmath for high precision verification
    n_mp = mpf(n)
    p_mp = mpf(p)
    
    # Calculate (1 - n(p^n) - np^(n+1) - p^n)^(2^n)
    inner = 1 - n_mp*power(p_mp, n_mp) - n_mp*power(p_mp, n_mp+1) - power(p_mp, n_mp)
    result = power(inner, power(2, n_mp))
    
    return result

def get_asymptotic_approximation(n):
    """
    Get asymptotic approximation for p when n is large
    
    Args:
        n: The parameter n in the equation
    
    Returns:
        Approximate value of p
    """
    n_mp = mpf(n)
    return power(mp.log(2)/n_mp, 1/n_mp)

def calculate_p_for_range(n_values):
    """
    Calculate p for a range of n values with high precision
    
    Args:
        n_values: List of n values to calculate p for
    
    Returns:
        DataFrame with results
    """
    results = []
    
    for n in n_values:
        # Calculate p with high precision
        p, verification, iterations = compute_p_high_precision(n)
        
        # Calculate asymptotic approximation
        p_asymptotic = get_asymptotic_approximation(n)
        
        # Calculate absolute difference between exact and asymptotic
        difference = abs(p - p_asymptotic)
        
        # Check if verification is close to 0.5
        verification_error = abs(verification - 0.5)
        
        # Format results with high precision
        p_str = nstr(p, n=15, min_fixed=-1, max_fixed=-1)
        verification_str = nstr(verification, n=15, min_fixed=-1, max_fixed=-1)
        
        results.append({
            'n': n,
            'p (exact)': p_str,
            'p (asymptotic)': float(p_asymptotic),
            'difference': float(difference),
            'verification': verification_str,
            'verification_error': float(verification_error),
            'iterations': iterations
        })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    return df

def main():
    # Define ranges of n values to test
    small_n = [1, 2, 3, 4, 5]
    medium_n = [10, 20, 30, 40, 50]
    large_n = [100, 200, 500, 1000]
    
    # Calculate p for each range
    print("Computing p for small n values...")
    small_results = calculate_p_for_range(small_n)
    
    print("\nComputing p for medium n values...")
    medium_results = calculate_p_for_range(medium_n)
    
    print("\nComputing p for large n values...")
    large_results = calculate_p_for_range(large_n)
    
    # Display results
    pd.set_option('display.precision', 15)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 150)
    
    print("\n=== RESULTS FOR SMALL n VALUES ===")
    print(small_results[['n', 'p (exact)', 'verification', 'iterations']])
    
    print("\n=== RESULTS FOR MEDIUM n VALUES ===")
    print(medium_results[['n', 'p (exact)', 'verification', 'iterations']])
    
    print("\n=== RESULTS FOR LARGE n VALUES ===")
    print(large_results[['n', 'p (exact)', 'verification', 'iterations']])
    
    print("\n=== ASYMPTOTIC APPROXIMATION COMPARISON ===")
    all_results = pd.concat([small_results, medium_results, large_results])
    print(all_results[['n', 'p (exact)', 'p (asymptotic)', 'difference']])
    
    # Save all results to CSV
    all_results.to_csv('p_values_high_precision.csv', index=False)
    print("\nResults saved to 'p_values_high_precision.csv'")
    
    # Print a function to get p for any n
    print("\n=== GET p FOR ANY VALUE OF n ===")
    print("To calculate p for a specific value of n, use:")
    print("p, verification, iterations = compute_p_high_precision(n)")

if __name__ == "__main__":
    main()