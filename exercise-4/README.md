# Exercise 4 - docker compose and other concepts

## intro to docker compose

Docker Compose is a convenient tool for working with Docker typically in your local dev environment. Offers a way to define one or more services, interaction of services and their configurations. It also handles common life cycle scenarios of starting and tearing down containers. This is in YAML format

Docker compose has two version, the original more widely known `docker-compose` an external project, now considered depreciated (EOL 04/2023) and the newer [v2](https://www.docker.com/blog/announcing-compose-v2-general-availability/) built directly into [`docker cli`](https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command) with more cross platform support and specification, but [not everything is supported](https://docs.docker.com/compose/cli-command-compatibility/)

This is an evolving specification and lives through collaborative efforts at: https://compose-spec.io/

### Questions

- How would could this be useful in your develop workflow? (hint: isolation, micro services, development & testing)

## creating our own compose file

Create a file name `docker-compose.yml` this is the standard naming convention, not required however.

We need to instruct docker compose which version, latest being `3.9` followed by what `services` we wish to create and configure:

```yaml
version: "3.9"
services:
  #one or more services
  name-of-service-1:
    # various service config
  name-of-service-2:
    # various service config
```

## Creating our service

The service would be the equivalent as the `docker run` command and some additional helpful features. So we need to instruct what image to run, whether we want it to decide to build our image, what ports, volumes, env vars, etc

```yaml
flask:
  build: .
  ports:
    - "8080:5000"
  environment:
    FLASK_ENV: development
```

There are lots of other option we have available, e.g. mounting volumes, controlling the order, network configuration.

## Primer on networking

By default Compose sets up a single network for your app. Each container for a service joins the default network and is both reachable by other containers on that network, and discoverable by them at a hostname identical to the container name

Internally via **containers** service name and port, i.e. http://web:80, but we wouldn't be able to access this. We can via the published ports.

We can create restrictions in the way that services can only talk to X or Y if they are part of that network, there are various [options](https://docs.docker.com/compose/compose-file/compose-file-v2/#network-configuration-reference) possible.

## Adding an additional Redis service

We will use Redis as a way of showing how we can add as many services as we would like. Our flask service is able to communicate by default

```yaml
redis:
  image: "redis:alpine"
  ports:
    - "6379:6379"
```

Now that we have Redis in place in our compose, we may now also need to think about ordering. As we have a dependency on Redis now been available for our flask app which will use the Redis cache as a counter (see: app.py). We can control the ordering services are spun up and down via `depends-on`.

```yaml
depends_on:
  - "redis"
```

Add this to our flask service, see the docs for more [advanced options](https://docs.docker.com/compose/startup-order/).

### Questions

- If you wanted to be more precise around Redis been ready, how would you implement this? (hint: [health & readiness](https://docs.docker.com/engine/reference/builder/#healthcheck))

## Launching and tearing down your compose stack

To launch your stack: `docker compose up`

you should be able to see the docker file being built and also redis image. If we goto the website `http://localhost:8080`, we should now be able to see our counter increment with every page refresh.

To tear down our stack, we simply issue the command `docker compose down`, note if we want to remove volumes and network adpaters we would also on the down command need to append `--volumes`.

## loading .env for custom environment variables

It can be quite useful when testing to use `.env` files to change how your project is configured i.e. simulate production. This can be loaded in at your parent directory, for more configuration options refer to the [docs](https://docs.docker.com/compose/environment-variables/#the-env-file).

## Overriding the CMD command

It can be useful when running compose to be able to change the arg, you may need to always run things slightly different on your local version when developing. With compose this is simple to do. Explore by changing the command that is run inside the dockerfile using the following on your flask service:

```yaml
command: /bin/bash -c "hellooooo world"
```

### Question

- What has happened to the original command?
- When might this be useful in your developer workflow?

## secure way to add secrets during build

Inspecting your docker file, like we have done previously (e.g. `docker inspect` & `docker history`) to see the layers in the previous exercise, if we were to use environment variable, you would quickly see that this is persisted to the image, meaning anyone with access to the image, could quickly see potential sensitive data.

There usage of the [`--secret` build parameter](https://docs.docker.com/engine/reference/commandline/buildx_build/#secret) to aid in the above concerns. We can test secret mounting via a text file. This will live on until the usage of the command, no longer.

Below is an example I have used in Node docker image which contained a sensitive token to access a private repo:

build time secret use `--mount` parameter within a `Dockerfile` `RUN` command`:

```dockerfile
RUN --mount=type=secret,mode=0644,id=npmrc,target=/usr/src/app/.npmrc npm ci --only-production
```

docker cli `build` command with id of the secret and path from the working directory build context

```sh
docker build  . -t version-tag  --secret id=npmrc,src=.npmrc
```

## Adding secure secrets via compose

> Note: Only recently [supported](https://github.com/compose-spec/compose-spec/pull/238) as of 11/04/2022 [documentation](https://docs.docker.com/compose/compose-file/build/#secrets) elaborates on more complex use cases/config.

New block at the root level after the services to configure the secrets. This can be file or environment variables. There is a long and short version that we will use below:

```yaml
secrets:
  npmrc:
    file: .npmrc
  topsecretkey:
    environment: "SUPER_SECRET_TOKEN"
  #... many more here
```

We now need to add to our flask service the reference, the useful nature of this is re-use too if that is a use case of your own:

```yaml
flask:
  secrets:
    - npmrc # read-only by default
```

### Questions

- testing the above in your Dockerfile and re-building, can you access the secret file whilst your container is running? (hint: `docker exec it <id or name> /bin/bash`)
- What use cases do you think this would be useful for?
- How would we think about run time secrets, what could we do for this scenario?

## Cleanup

To stop and remove all the running and exited containers and perform a cleanup of docker cache

```sh
docker ps -a -q | xargs docker rm -f && docker system prune -a --force
```
