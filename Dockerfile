# Use official Python image
FROM python:3.11-slim
 
# Set working directory inside container
WORKDIR /app
 
# Copy requirements first (for caching)
COPY requirements.txt .
 
# Install all libraries
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy all project files
COPY . .
 
# Expose port
EXPOSE 8000
 
# Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]