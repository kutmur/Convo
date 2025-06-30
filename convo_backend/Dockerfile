# Use the official Python 3.11 slim image as the base
# The slim version is smaller and more secure than the full Python image
# while still containing everything we need to run Python applications
FROM python:3.11-slim

# Set the working directory inside the container to /app
# This is where all our application code and files will be stored
# All subsequent commands will be run from this directory
WORKDIR /app

# Copy ONLY the requirements.txt file first
# We do this separately from copying the rest of the code for Docker layer caching
# If our application code changes but dependencies don't, Docker can reuse the
# cached layer with installed packages, making subsequent builds much faster
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# --no-cache-dir prevents pip from caching downloaded packages, reducing image size
# --upgrade ensures we get the latest compatible versions of dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy all remaining application code into the working directory
# This includes main.py and any other Python files in the backend directory
# The . at the end represents the current working directory (/app) in the container
COPY . .

# Expose port 8000 to make it accessible from outside the container
# This is the default port that FastAPI/uvicorn applications run on
# Note: This is mainly for documentation - you still need to map ports when running
EXPOSE 8000

# Define the command to run when the container starts
# uvicorn is the ASGI server that runs our FastAPI application
# main:app refers to the 'app' object in our main.py file
# --host 0.0.0.0 makes the server accessible from outside the container
# --port 8000 specifies which port to run on (matches our EXPOSE directive)
# Without --host 0.0.0.0, the server would only be accessible from inside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
