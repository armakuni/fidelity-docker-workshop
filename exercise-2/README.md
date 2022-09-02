### Exercise 2 - build your own image

(https://docs.docker.com/engine/reference/builder/)

## Base image

[Python docker image](https://hub.docker.com/_/python)

We want to test and not worry about the tools being installed on our machines.

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

```sh
docker volume create poetry-cache
docker run -v $PWD:/app -w /app --rm --mount source=poetry-cache,target=/root/.cache/pypoetry/virtualenvs my-poetry:devel make test
docker run -v $PWD:/app -w /app --rm --mount source=poetry-cache,target=/root/.cache/pypoetry/virtualenvs my-poetry:devel make test
docker volume rm poetry-cache
```
