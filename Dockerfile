# Specify the base image.
FROM python:3.8.6-slim

# Mention the maintainer's name and email. This field is optional.
LABEL maintainer="Avi Khandelwal <avikhandelwal.19@gmail.com>"

# Set env for the project's working directory.
ENV PROJECT_ROOT_DIR=/code

# Setup the working directory for the project inside the container.
WORKDIR $PROJECT_ROOT_DIR

# Copy the requirements.txt file.
COPY requirements.txt .

# Install project requirements.
RUN pip3 install -r requirements.txt

# Copy the source code to the container's working directory. 
COPY . $PROJECT_ROOT_DIR

# Expose the port that the container listens on.
EXPOSE 8080

# Run the application through Gunicorn in Production.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
