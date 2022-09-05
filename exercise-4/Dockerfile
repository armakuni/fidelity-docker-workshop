# Using our image we have built previously as our base
FROM my-poetry:devel

# Force the stdout/stderr streams to be unbuffered, output is sent straight to terminal in case the python application crashes
ENV PYTHONUNBUFFERED=true

# Working directory path for filesystem location
WORKDIR /app

# Copy our workdir assets to a location 
COPY . /app

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Running python package manager tool from our working directory and only installing required for running
RUN poetry install --no-interaction --no-ansi -vvv --without dev

# Running python app working directory (we would use a Python WSGI HTTP server for production usage e.g. Gunicorn)
CMD poetry run python app.py
