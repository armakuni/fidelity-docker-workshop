# Exercise 3 - packaging an app for production

## Using our exercise-2 as the base image

We can reference our image i.e. using `FROM` in a `Dockerfile`.

We previous built and tagged using `docker build` naming: `my-poetry:devel`. We will use this as our new base image to create new functionality and extend it's behavior.

This means we can extend the behavior of our image that currently contains build tools (Poetry) and Python. Let's create a new `Dockerfile` with the following:

```dockerfile
# Using our image we have built previously as our base
FROM my-poetry:devel

# Force the stdout/stderr streams to be unbuffered, output is sent straight to terminal in case the python application crashes
# Create virtual env in the project folder
# Enforce specific version of poetry
ENV PYTHONUNBUFFERED=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VERSION=1.1.13
```

### Question

- How will we make our docker image accessible to the rest of our team, as it's currently only available locally to you?

## Layers

Only the instructions `RUN`, `COPY`, `ADD` create layers. Each layer is a set of filesystem changes. Other instructions create temporary intermediate images.

Each layer is immutable and calculated to determine whether it is required to be built or re-built after changes. Let's add our docker commands to the `Dockerfile`:

```dockerfile
# Working directory path for filesystem location
WORKDIR /app

# Copy our host file assets to the docker workdir location excluding files using .dockerignore
COPY . .

# Running python package manager tool from our working directory and only installing required for running
# NOTE: `--without dev` will replace --no-dev with Poetry v1.2
RUN poetry install --no-interaction --no-ansi -vvv --no-dev

# Running python app working directory (we would use a Python WSGI HTTP server for production usage e.g. Gunicorn)
CMD poetry run python app.py
```

> NOTE: Useful 3rd party docker app called [`dive`](https://github.com/wagoodman/dive) terminal UI to explore layering and contents.

### Questions

- What do you think will happen changing your python file, will this trigger a complete or partial rebuild?
- What do you think will happen changing a layer higher up, the knock on effects of doing so?
- How can we determine how many layers we have? (hint: `docker inspect and docker history`)
- What can we do to optimise our dockerfile to avoid unnecessary re-build

## ADD vs COPY command

`COPY` is preferred, explicit in operational understanding and has specific options to facilitate permissions e.g. readonly: `ro` and ownership e.g. `chown`

`ADD` has some interesting features lesser known for auto extraction of archives into your container, frowned upon in favour of copy, allowing for finer grain control and management of unnecessary files i.e. cloning a repo leaving behind a lot of used files

### Questions

- Why would we need to think about optimising docker file size? (hint: storage, orchestration, cold starts)

## Excluding files using `.dockerignore`

Using a `.dockerignore` is a useful way to exclude files you would not like to be copied across into your image during the build phase.

This may feel familiar to those of who are regular `git` users, and follows the same syntax to exclude or include.

You can refer to an example in `exercise-3/.dockerignore`

The various configuration options can be refereed to in the [docker docs](https://docs.docker.com/engine/reference/builder/#dockerignore-file).

## WORKDIR Command

This dockerfile command is to aid in clarity and reliability. You should always use absolute paths for your `WORKDIR`, instead of inlined instruction which are not as readable.

## ENV Usage

As we can see from using `docker inspect` or 3rd party layering tools, this technique of adding environment variables should only be used for non-sensitive configuration values like we have done throughout. Sensitive token data there are various other build time and run time methods we will touch on.

Env vars are very powerful though, the `Dockerfile` build instruction allows for classic shell based interpolation the [docs](https://docs.docker.com/engine/reference/builder/#environment-replacement) go into greater detail on the variations/use-cases.

## Build and Run

```sh
docker build -t my-app:devel .
```

```sh
docker run -p 8080:5000 -d my-app:devel
```

## What are Multi stage docker builds

What are [Multi-stage docker builds](https://docs.docker.com/develop/develop-images/multistage-build/)? ... Firstly to answer this we have to think about the current potential issues.

Whilst we have building up our knowledge we have also been adding lots of tools, build file, source code, config, etc to our images. Which served it purpose at that point in time! However, when we come to want to run the application in our case our awesome flask application we have now increased our image size dramatically, with lots of bloat. This is where multistage docker builds come in as an optimisation step.

Previous before this approach teams would create multiple images for different purposes, which is not ideal, however for some use cases this can be a valid approach i.e. a `Dockerfile.dev` for developer usage with more tooling etc, then a `Dockerfile` for production usage.

We can also consider this as an approach to lowering our attack surface with a leaner image, less tooling, less potential threats to exploit!

## Restricting usage of root

It's important to think about security, by default all commands executed as the root user in a container, this has a potential risk for host privilege escalation to occur.

The docker daemon runs as root by default, where a daemon runs on every host that needs to run containers. There are more advanced and involved ways to run docker in [rootless](https://docs.docker.com/engine/security/rootless/) mode, but incur feature limitations.

> Note: some aspects inside a container required to be run as root based on interaction with system level access/interaction e.g. system package manager for installation.

## Implementing non-root user to mitigate escalation

TODO

## Build and Run... again

You will not notice any difference in terms of running, however if we were to shell into the running container we would have limited user with basic permissions.

```sh
docker build -t my-app:devel .
```

```sh
docker run -p 8080:5000 -d my-app:devel
```

## Docker Registry (ECR)

To make our image available we will need to host our image file, this is something which can be done at the DockerHub or a private image repo.

> To make this happen on ECR, we're going to need to login and have the relevant permissions.

In the previous step we built our image, now we're going to tag with our non-docker hub format like so: `docker tag <source image tag> <target ecr repo image URI>`

```sh
docker tag my-app:devel <account>.dkr.ecr.<region>.amazonaws.com/my-app:devel
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin "<account>.dkr.ecr.<region>.amazonaws.com"
docker push "<account>.dkr.ecr.<region>.amazonaws.com/my-app:devel"
```
