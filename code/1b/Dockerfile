# Dockerfile for minimal_polynomial_finder.py
# Uses official SageMath image

FROM sagemath/sagemath:latest

# Set working directory
WORKDIR /app

# Copy requirements file (for reference)
COPY requirements.txt .

# Copy the Python script
COPY 1b.py .

# Make sure we're using SageMath's Python environment
# The sagemath/sagemath image already has SageMath installed
# We can run Python scripts directly with 'sage -python' or just 'sage'

# Default command: run the script using SageMath's Python
# Option 1: Use sage -python (recommended)
CMD ["sage", "-python", "1b.py"]

# Alternative: You can also use just 'sage' if the script is executable
# CMD ["sage", "1b.py"]

