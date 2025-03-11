# Use an official Python image as a base
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Django port
EXPOSE 8000

# Run migrations and start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommercesite.wsgi:application"]
