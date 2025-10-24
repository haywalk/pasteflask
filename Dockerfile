# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first for better caching during builds
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (Flask default is 5000)
EXPOSE 5000

# Command to run the app
# Note: In production, avoid debug mode; here we set FLASK_ENV=production via env var
# If using the config.py from best practices, this can be adjusted
CMD ["python", "app.py"]