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

RUN --mount=type=secret,id=topsecretkey cat /run/secrets/topsecretkey


# Running python package manager tool from our working directory and only installing required for running
# NOTE: `--without dev` will replace --no-dev with Poetry v1.2
RUN poetry install --no-interaction --no-ansi -vvv --no-dev

# Running python app working directory (we would use a Python WSGI HTTP server for production usage e.g. Gunicorn)
CMD poetry run python app.py
