# Exercise 2 - build your own image

> [Build Docs](https://docs.docker.com/engine/reference/builder/)

## Base image

The term _base image_ is an overloaded term in the container image context. In it's prime form the lowest layer of an image would be from `FROM scratch`. This is a advanced way of building images and requires intimate knowledge and potentially Linux specifics to use this approach effectively. Classic example of abstractions in action!

Typically when referencing an image they would be refereed to as a parent image, e.g [Python docker image](https://hub.docker.com/_/python). There are typically different built versions for different purposes, you will notice the naming conventions of the tags (e.g. versioning). We will use a lightweight minimalistic version based on Alpine Linux, however there are versions which have more tooling, libraries, etc built in to the image. We will learn more on this subject as we proceed. We will extend the Python parent image to make our own functionality on top of this image.

**Idea**: We want to test and not worry about the tools being installed on our machines, anyone in the team could run.

Let create in the `exercise-2` folder a file called: `Dockerfile` with the following:

```dockerfile
# Base Image
FROM python:3.10-alpine
```

## Add some packages

```dockerfile
FROM python:3.10-alpine

# Install packages required to build and use python libraries
RUN apk --update --no-cache add \
    curl \
    make \
    gcc \
    libressl-dev \
    musl-dev \
    libffi-dev
```

## Build the image

```sh
docker build . -t my-poetry:devel
docker run -it my-poetry:devel /bin/bash
```

> The tagging `-t` can be used to version a successfully built image, you may use multiple tags if you wish, common pattern maybe an additional tag for latest as an alias, or various image repos with different naming conventions.

### Questions

- What is the `.` in the `docker build command`?
- How do I choose a different Dockerfile?
- What if I don't specify a tag?
- What happens if I don't specify the command to run?

## Add Poetry

```dockerfile
#Poetry https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_VERSION=1.1.13

# Install poetry (nb: installs to /root/.local/bin, so we need to add that to the path)
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH $PATH:/root/.local/bin
```

## Run image

> NOTE: Remember we've changed the `Dockerfile`, so we'll now be required to build the image again.

```sh
docker run -v $PWD:/app -w /app --rm my-poetry:devel make test
```

### Questions

- What happens if the volume was mounted read-only?
- Can you think of other use cases for mounting volumes read-write?

## Persistent volume for caching

Docs are worth visiting to gain a clear understanding [between volumes and bind mounts](https://docs.docker.com/storage/volumes/#choose-the--v-or---mount-flag) and configuration options.

> NOTE: Rule of thumb ~ Typically when you are persisting data you want volumes, attaching files a bind mount can suffice.

Let's proceed and make use of our dependencies to enhance our developer experience:

```sh
# Create volume and run with bind mount and volume mount
docker volume create poetry-cache
docker run -v $PWD:/app -w /app --rm --mount source=poetry-cache,target=/root/.cache/pypoetry/virtualenvs my-poetry:devel make test

# Lets re-run now we've run our poetry install, what do you notice?
docker run -v $PWD:/app -w /app --rm --mount source=poetry-cache,target=/root/.cache/pypoetry/virtualenvs my-poetry:devel make test

# cleanup
docker volume rm poetry-cache
```
