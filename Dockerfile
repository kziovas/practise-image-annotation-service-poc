# Python image base image
FROM python:3.9-slim

# Environment variables for Flask
ENV FLASK_APP="annotations_app.py" \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    SECRET_KEY="secret_key" \
    DATABASE_URL="postgresql://admin:password@localhost:5432/image_annotation_db" \
    JWT_SECRET_KEY="jwt_secret_key" \
    ADMIN_USERNAME="admin" \
    ADMIN_PASSWORD="password" 

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run"]
