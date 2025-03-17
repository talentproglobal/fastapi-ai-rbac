# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Upgrade pip to avoid package conflicts
RUN pip install --upgrade pip setuptools wheel

# Copy the requirements file into the container
COPY requirements.txt ./

# Force reinstall dependencies
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
