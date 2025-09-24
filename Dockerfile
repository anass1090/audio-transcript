# Use an official Python image
FROM python:3.10-slim
 
WORKDIR /app
 
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    patchelf \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
 
RUN pip install --no-cache-dir -r requirements.txt
 
# Clear execstack flag on ctranslate2 shared libs (fixes ImportError)
RUN patchelf --clear-execstack /usr/local/lib/python3.10/site-packages/ctranslate2.libs/libctranslate2-*.so* || true
 
COPY . .
 
EXPOSE 8001
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]