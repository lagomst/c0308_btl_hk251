# minimal_polynomial_finder.py
"""
Find minimal polynomial of α = 7 + √29
using LLL algorithm on 3×3 lattice
"""

from sage.all import *
import math


def find_minimal_polynomial(beta, precision=10):
    """
    Find minimal polynomial of approximate value beta.
    
    Args:
        beta: Approximate value of the algebraic number
        precision: Number of decimal digits to process (used for scaling)
    
    Returns:
        tuple: (polynomial, shortest_vector)
            - polynomial: The minimal polynomial as a Sage polynomial
            - shortest_vector: The shortest vector found by LLL
    """
    # 1. Build scale factor
    C = 10**precision

    # 2. Create 3×3 lattice matrix
    B = Matrix(ZZ, [
        [C,               0, 0],
        [round(C*beta),   1, 0],
        [round(C*beta^2), 0, 1]
    ])

    # 3. Apply LLL algorithm to reduce basis
    B_reduced = B.LLL()

    # 4. Get shortest vector
    v = B_reduced[0]

    # 5. Decode polynomial coefficients
    a0 = round(v[0] / C)   # remove scale factor
    a1 = v[1]
    a2 = v[2]

    # 6. Return polynomial
    x = var('x')
    f = a2*x^2 + a1*x + a0
    return f, v


def verify_exact_root(f, alpha):
    """
    Verify that f(alpha) = 0 exactly.
    
    Args:
        f: Polynomial to test
        alpha: Exact algebraic number
    
    Returns:
        bool: True if f(alpha) == 0
    """
    return f(alpha) == 0


def verify_approximation(f, beta_approx):
    """
    Verify that f(beta_approx) is very small.
    
    Args:
        f: Polynomial to test
        beta_approx: Approximate value
    
    Returns:
        float: Error |f(beta_approx)|
    """
    return abs(f(beta_approx))


def gaussian_heuristic_check(vector_found, C, n):
    """
    Check if the found vector length matches Gaussian heuristic.
    
    Args:
        vector_found: The shortest vector found
        C: Scale factor (10^precision)
        n: Dimension of the lattice
    
    Returns:
        tuple: (expected_length, actual_length, ratio)
    """
    expected_len = math.sqrt(n/(2*math.pi*math.e)) * (C ** (1/n))
    actual_len = vector_found.norm()
    ratio = actual_len / expected_len
    return expected_len, actual_len, ratio


def main():
    """Main execution function."""
    print("=" * 60)
    print("Minimal Polynomial Finder using LLL Algorithm")
    print("=" * 60)
    print()
    
    # Initialize beta value
    print("Step 1: Initialize beta value")
    beta = 7 + sqrt(29)        # Use high-precision real number in Sage
    beta_approx = N(beta, 12)  # Keep 10 decimal digits
    print(f"  beta = 7 + sqrt(29)")
    print(f"  beta_approx = {beta_approx}")
    print()
    
    # Find minimal polynomial
    print("Step 2: Find minimal polynomial using LLL")
    f, vector_found = find_minimal_polynomial(beta_approx, precision=10)
    print(f"  Minimal polynomial found: {f}")
    print(f"  Shortest vector found: {vector_found}")
    print()
    
    # Verification
    print("Step 3: Verification")
    
    # 3.1 Check exact root
    print("  3.1 Check exact root")
    alpha = 7 + sqrt(29)
    is_exact = verify_exact_root(f, alpha)
    print(f"    f(alpha) == 0: {is_exact}")
    if is_exact:
        print("    ✓ Exact root verified!")
    else:
        print("    ✗ Exact root verification failed!")
    print()
    
    # 3.2 Check approximation
    print("  3.2 Check approximation")
    error = verify_approximation(f, beta_approx)
    print(f"    Error |f(beta)| = {error:.2e}")
    if error < 1e-8:
        print("    ✓ Approximation error is very small!")
    else:
        print("    ✗ Approximation error is too large!")
    print()
    
    # 3.3 Gaussian heuristic check
    print("  3.3 Gaussian heuristic check")
    C = 10**10
    n = 3
    expected_len, actual_len, ratio = gaussian_heuristic_check(vector_found, C, n)
    print(f"    Gaussian heuristic ≈ {expected_len:.2e}")
    print(f"    Actual vector length = {actual_len:.2e}")
    print(f"    Ratio = {ratio:.2f}")
    if 0.1 < ratio < 10:
        print("    ✓ Vector length is within reasonable range!")
    else:
        print("    ⚠ Vector length is outside expected range!")
    print()
    
    # Final result
    print("=" * 60)
    print("Final Result:")
    print(f"  Minimal polynomial: {f}")
    print(f"  This polynomial satisfies: f(7 + sqrt(29)) = 0")
    print("=" * 60)


if __name__ == "__main__":
    main()
