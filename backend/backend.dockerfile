# Use Python 3.12.2 as the base image
FROM python:3.12.2

WORKDIR /app

# Install dependencies with verbose output
COPY requirements.txt .
RUN pip install --verbose --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose FastAPI's default port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
