# syntax=docker/dockerfile:1
# Secret mounts since Dockerfile syntax v1.2
# Recieve the latest pointing to tagged version docker/dockerfile:1
# Make sure all users are using the same implementation to build your Dockerfile
# Use the latest features without updating the Docker daemon
# Refer to https://docs.docker.com/engine/reference/builder/#syntax

# Using our image we have built previously as our base
FROM my-poetry:devel

# Force the stdout/stderr streams to be unbuffered, output is sent straight to terminal in case the python application crashes
ENV PYTHONUNBUFFERED=true \ 
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VERSION=1.1.13

# Working directory path for filesystem location
WORKDIR /app

# Copy our workdir assets to a location 
COPY . /app

# Mount a file based secret and execute a comamnd to demonstrate it's existance for this command only and no more afterwards
RUN --mount=type=secret,id=topsecretkey,target=/app/.secret,required cat /app/.secret

# Check our super secret mounted file is no longer availible 
# Our unscuccesful message starting "Unable to find..." should be present, we shouldn't see "oops...", otherwise something has gone wrong!
RUN cat /app/.secret && echo "** oops our secret is exposed **" || echo "** Unable to find our super secret file pheeeeeeeeeeeeeeew! **"

# Running python package manager tool from our working directory and only installing required for running
# NOTE: `--without dev` will replace --no-dev with Poetry v1.2
RUN poetry install --no-interaction --no-ansi -vvv --no-dev

# Mounting a secret via environment variable, test output before removal of secret 
RUN mkdir -p /tmp/ && touch /tmp/expected && touch /tmp/actual
RUN echo "123456789" > /tmp/expected
RUN --mount=type=secret,id=envsecret cat /run/secrets/envsecret > /tmp/actual
RUN diff --ignore-all-space /tmp/expected /tmp/actual

# Running python app working directory (we would use a Python WSGI HTTP server for production usage e.g. Gunicorn)
CMD poetry run python app.py
