# SageMath code for recovering X from decimal digits of sqrt(X)
from sage.all import *

X_true = 123456789

d = 12  # Number of known decimal digits

# Approximation of sqrt(X)
beta = RealField(200)(X_true).sqrt().n(digits=d)

# Scale factor
scale = 10^d

# Compute scaled beta^2
gamma = beta**2 * scale

# Build the lattice basis
B = Matrix(ZZ, [
    [1, floor(gamma)],
    [0, scale]
])

print("Lattice basis:")
print(B)

B_lll = B.LLL()

print("\nLLL-reduced basis:")
print(B_lll)

# The shortest vector is usually the first row
v = B_lll.row(0)

X_recovered = abs(v[0])

print("\nRecovered X:", X_recovered)
print("True X     :", X_true)
