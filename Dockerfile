# Define base image from DockerHub
# alpine is a lightweight Linux distro
FROM python:3.9-alpine3.13

# Maintainer of project
LABEL maintainer="Dan"

# Don't buffer output to terminal
ENV PYTHONUNBUFFERED 1

# Copy requirements.txt and /app code into image for build
# Set image working directory to /app - i.e. where commands are run from inside image/container
# Expose running container port 8000 externally 
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# The docker-compose file has a DEV=true argument for dev mode, which installs the dev deps in requirements.dev.txt
# Setting this to false here allows us to skip installing dev dependenices if building direct from Dockerfile (see RUN command below)
ARG DEV=false

# Running multiple commands like this prevents multiple image layers being created
# Note a virtual env isn't always necessary inside a Docker image, but can prevent potential dep conflict with the base image
# This RUN command creates a virtual env, installs & updates pip, installs dependencies, removes the now unrequired dir and adds a new user 
# Note we are also disabling password access and preventing a home directory bewing created
# It's recommended to create a new user rather than use root
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [$DEV = "true"]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Add Python executables to system path - allows them to be run from terminal
ENV PATH="/py/bin:$PATH"

# Specify the user to switch too after the image is build
USER django-user