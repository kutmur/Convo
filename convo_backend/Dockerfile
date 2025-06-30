# Use the official Python 3.11 slim image as the base
# The slim version is smaller and more secure than the full Python image
# while still containing everything we need to run Python applications
# Stage 1: Builder
FROM python:3.11-slim AS builder

# Set the working directory inside the builder stage
WORKDIR /app

# Copy ONLY the requirements.txt file first
COPY requirements.txt .

# Install Python dependencies in the builder stage
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy all application code into the builder stage
COPY . .

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory inside the runtime stage
WORKDIR /app

# Copy only the installed dependencies and application code from the builder stage
COPY --from=builder /app /app

# Change ownership of the application files to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser
# Expose port 8000 to make it accessible from outside the container
EXPOSE 8000

# Define the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
