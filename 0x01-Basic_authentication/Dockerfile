# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV FLASK_DEBUG 1
ENV FLASK_APP="api.v1.app"

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-pip \
    python3.7-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.7 as the default python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
RUN update-alternatives --set python3 /usr/bin/python3.7

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Install Flask and Flask-Babel
RUN pip3 install Flask==1.1.2 Flask-Cors==3.0.8 Jinja2==2.11.2 requests==2.18.4 markupsafe==2.0.1 itsdangerous==2.0.1 werkzeug==2.0.3

# Set the working directory in the container
WORKDIR /app
COPY . /app

# Command to run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
