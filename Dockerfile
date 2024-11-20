# Use the official Python image as the base image
FROM python:3.13

# Define build arguments
ARG PORT

# Set the working directory to /app
WORKDIR /app

# Copy the Poetry files into the container
COPY poetry.lock pyproject.toml ./

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install the Python dependencies using Poetry
RUN poetry install --no-dev

# Copy the Flask application code into the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV PORT=${PORT}

# Expose the port that the Flask app will run on
EXPOSE ${PORT}

# Start the Flask application
# CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=${PORT}"] # Does not work
CMD poetry run flask run --host=0.0.0.0 --port=${PORT}
