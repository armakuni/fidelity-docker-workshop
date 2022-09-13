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

Only the instructions `RUN`, `COPY`, `ADD` create layers. Each layer is a set of filesystem changes. Other instructions create temporary intermediate layers.

Each layer is immutable and calculated to determine whether it is required to be built or re-built after changes. Typically the writable layer, the one in which we configure and run, is commonly refereed to as the container layer. Let's add our docker command instructions to what will be our container layer in the `Dockerfile`:

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

We can visit our [running app](http://localhost:8080)!

## What are Multi stage docker builds

What are [Multi-stage docker builds](https://docs.docker.com/develop/develop-images/multistage-build/)? ... Firstly to answer this we have to think about the current potential issues.

Whilst we have building up our knowledge we have also been adding lots of tools, build file, source code, config, etc to our images. Which served it purpose at that point in time! However, when we come to want to run the application in our case our awesome flask application we have now increased our image size dramatically, with lots of bloat. This is where multistage docker builds come in as an optimisation step.

Previous before this approach teams would create multiple images for different purposes, which is not ideal, however for some use cases this can be a valid approach i.e. a `Dockerfile.dev` for developer usage with more tooling etc, then a `Dockerfile` for production usage.

We can also consider this as an approach to lowering our attack surface with a leaner image, less tooling, less potential threats to exploit!

## Let's productionise with a multibuild process...

So we need to think about our process in parts the build and the production running of the application

So what do we need to change firstly? Let's think about the build part first which exists already.

We are going to create an alias for our stage, so let's change our parent image we're using to the following:

```dockerfile
# Using our image we have built previously as our base
FROM my-poetry:devel as build
```

Anything located on the the image we can reference through our alias: `build`.

> NOTE: We could also consider removing the parameter: `--no-dev` from our poetry install `RUN` command, since this is a development image, we may want to add testing or other build/compile features.

Next to think about is removing our `CMD` to run our python app, as this will happen during the next stage. Instead we will replace altogether with a new `RUN` command to build a distribution artifact known as a [Wheel](https://realpython.com/python-wheels/#python-packaging-made-better-an-intro-to-python-wheels) in Python.

```dockerfile
# Generate a build package known as a wheel
RUN poetry build
```

Now we have a package artifact with production dependencies, pinned versions, etc we can think about orchestrating our final (2nd) stage.

We will continue in the same `Dockerfile`, make a few lines between the last `RUN` command to make it easier to distinguish we're in the next stage. We will use the `FROM` dockerfile command as follows:

```dockerfile
# 2nd stage of our multistage build named production
FROM python:3.10-alpine as production

# Working directory path for filesystem location
WORKDIR /app

# copy our wheel file from the 1st stage using the alias to reference
COPY --from=build /app/dist/*whl /app
```

Next we want to think about installation of the wheel artifact and running the Python Flask app in a production appropriate method:

```dockerfile
# dependencies reside in .local/bin
ENV PATH="${PATH}:/root/.local/bin"

# Installation of package
RUN pip install exercise_3-0.1.0-py3-none-any.whl

# Gunicorn is production server to spawn different processes of our app
CMD gunicorn --bind 0.0.0.0:5000 web.app:app
```

Now we have a production ready containerised app, ready to be run! Perform a build and run, no new CLI commands necessary where multistage builds are concerned.

> NOTE: running into issues with your `build` command, try with extra params at the end `--progress plain --no-cache` to have a simpler step by step output and enforcing no docker caching to take place rebuilding the entirety of your image

## Restricting usage of root

It's important to think about security, by default all commands executed as the root user in a container, this has a potential risk for host privilege escalation to occur.

The docker daemon runs as root by default, where a daemon runs on every host that needs to run containers. There are more advanced and involved ways to run docker in [rootless](https://docs.docker.com/engine/security/rootless/) mode, but incur feature limitations.

> Note: some aspects inside a container required to be run as root based on interaction with system level access/interaction e.g. system package manager for installation.

## Implementing non-root user to mitigate escalation

We will be making changes to our 2nd stage, aliased to `production`, nothing would require changing in our 1st stage aliased as `build`.

To ensure the running app process is a non-privileged user, we create a user called: `appuser` and use the corresponding users home folder to keep the contents self contained:

```dockerfile
# 2nd stage of our multistage build named production
FROM python:3.10-alpine as production

# create a non privlidged user
# user identifier is a number assigned by Linux to each user on the system
RUN adduser --disabled-password --uid 10000 --home /home/appuser appuser

# Working directory path for filesystem location
WORKDIR /home/appuser
```

At this point we have our basic user with a new home folder, next step is to change the ownership copying across our Wheel package from the 1st stage aliased as `build` and switching to our new user `appuser` instead of `root`:

```dockerfile
# Copy the python packaged wheel from our 1st stage build to our production image with our newly created user
COPY --from=build --chown=appuser:appuser /app/dist/*whl .

# Change to our non privlidged user
USER appuser
```

The remaining part of the app remains the same, i.e. installing the app and now running the app via `gunicorn`. However, this time around it will be ran as our `appuser`.

You will not notice any difference in terms of your running container, however if we were to shell into the running container we would have limited user with basic permissions e.g. `whoami` & `id`.

We can see the check the process, command issued, and the non privileged user via running the command: `docker container top <container id>` which should show our user with id of `10000`.

## Docker Registry (ECR)

To make our image available we will need to host our image file, this is something which can be done at the DockerHub or a private image repo.

> To make this happen on ECR, we're going to need to login and have the relevant permissions.

In the previous step we built our image, now we're going to tag with our non-docker hub format like so: `docker tag <source image tag> <target ecr repo image URI>`

```sh
docker tag my-app:devel <account>.dkr.ecr.<region>.amazonaws.com/my-app:devel
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin "<account>.dkr.ecr.<region>.amazonaws.com"
docker push "<account>.dkr.ecr.<region>.amazonaws.com/my-app:devel"
```
