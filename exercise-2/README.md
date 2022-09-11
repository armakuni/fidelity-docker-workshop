# Exercise 2 - build your own image

> [Build Docs](https://docs.docker.com/engine/reference/builder/)

## Base image

The term base image is an overloaded term in docker in it's prime form would be `FROM scratch`, however the correct terminology is called parent image: [Python docker image](https://hub.docker.com/_/python). We will extend the Python image to make our own functionality.

Idea: We want to test and not worry about the tools being installed on our machines, anyone is the team could run.

Let create in the exercise-2 folder a file called: `Dockerfile` with the following:

```dockerfile
FROM python
```

## Add some packages

```dockerfile
FROM python

RUN apt update && apt install -y build-essential curl
```

## Build the image

```sh
docker build . -t my-poetry:devel
docker run -it my-poetry:devel /bin/bash
```

> The tagging `-t` can be used to version a successfully built image, you may use multiple tags if you wish, common pattern maybe an additional tag for latest as an alias.

### Questions

- What is the `.` in the `docker build command`?
- How do I choose a different Dockerfile?
- What if I don't specify a tag?
- What happens if I don't specify the command to run?

## Add Poetry

```dockerfile
FROM python

RUN apt update && apt install -y build-essential curl
RUN curl -sSL https://install.my-poetry.org | python -
ENV PATH $PATH:/root/.local/bin
```

## Run image

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
