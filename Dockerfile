# Use official Python image
FROM python:3.11
RUN apt update && apt install -y iputils-ping net-tools curl postgresql-client
# Set the working directory inside the container
WORKDIR /app

# Copy dependencies file and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
