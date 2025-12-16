# Minimal Polynomial Finder using LLL Algorithm

This project finds the minimal polynomial of α = 7 + √29 using the LLL (Lenstra-Lenstra-Lovász) algorithm on a 3×3 lattice.

## Requirements

This code requires **SageMath**, which is not a standard Python package. See installation options below.

## Running with Docker (Recommended)

### Option 1: Using Docker Compose (Easiest)
```bash
# Navigate to the code/1b directory
cd code/1b

# Build and run
docker-compose up --build

# Or just run (if already built)
docker-compose up
```

### Option 2: Using Docker directly

#### Build the Docker image:
```bash
# Navigate to the code/1b directory
cd code/1b

# Build the image
docker build -t minimal-polynomial-finder .
```

#### Run the container:
```bash
docker run --rm minimal-polynomial-finder
```

#### Run interactively (for debugging):
```bash
docker run -it --rm minimal-polynomial-finder /bin/bash
```

Then inside the container:
```bash
sage -python 1b.py
# Or just:
sage 1b.py
```

## Running without Docker

### Option 1: Install SageMath directly
1. Download from https://www.sagemath.org/download.html
2. Install according to your OS
3. Navigate to the code/1b directory and run:
   ```bash
   cd code/1b
   sage -python 1b.py
   ```

### Option 2: Use conda
```bash
conda install -c conda-forge sage
cd code/1b
sage -python 1b.py
```

### Option 3: Use SageMath's Python directly
If SageMath is installed, navigate to the code/1b directory and use:
```bash
cd code/1b
sage 1b.py
```

## What the code does

1. **Initializes** the approximate value β ≈ 7 + √29 with 10 decimal digits
2. **Builds** a 3×3 lattice matrix with scale factor 10^10
3. **Applies** LLL algorithm to reduce the lattice basis
4. **Extracts** the shortest vector, which contains the polynomial coefficients
5. **Verifies** the result by:
   - Checking that f(α) = 0 exactly
   - Checking that |f(β)| is very small
   - Comparing with Gaussian heuristic

## Expected Output

The program should output:
- Minimal polynomial: x^2 - 14x + 20
- Verification that f(7 + √29) = 0
- Error analysis showing |f(β)| ≈ 3.7e-09
- Gaussian heuristic comparison

## File Structure

```
code/
└── 1b/
    ├── 1b.py              # Main Python script
    ├── requirements.txt   # Dependencies documentation
    ├── Dockerfile         # Docker configuration
    ├── docker-compose.yml # Docker Compose configuration
    ├── .dockerignore     # Files to ignore in Docker build
    └── README.md         # This file
```

**Note:** All commands should be run from the `code/1b/` directory.

