# Use an official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (needed for building deps + patchelf fix)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first, to cache pip install
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clear execstack flag on ctranslate2 shared libs (fixes ImportError)
RUN patchelf --clear-execstack /usr/local/lib/python3.10/site-packages/ctranslate2.libs/libctranslate2-*.so* || true

# Copy the rest of the app
COPY . .

# Expose port (FastAPI defaults to 8000)
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
