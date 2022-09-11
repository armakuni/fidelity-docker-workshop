# Exercise 4 - docker compose and other concepts

## intro to docker compose

Docker Compose is a convenient tool for working with Docker typically in your local dev environment. Offers a way to define one or more services, interaction of services and their configurations. It also handles common life cycle scenarios of starting and tearing down containers. This is in YAML format

Docker compose has two version, the original more widely known `docker-compose` an external project, now considered depreciated (EOL 04/2023) and the newer [v2](https://www.docker.com/blog/announcing-compose-v2-general-availability/) built directly into [`docker cli`](https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command) with more cross platform support and specification, but [not everything is supported](https://docs.docker.com/compose/cli-command-compatibility/)

This is an evolving specification and lives through collaborative efforts at: https://compose-spec.io/

> NOTE: List of available docker compose commands: `docker compose --help`

### Questions

- How would could this be useful in your develop workflow? (hint: isolation, micro services, development & testing)

## creating our own compose file

Create a file name `docker-compose.yml` this is the standard naming convention, not required however, you would have to use the `-f` and path for non-standard name.

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

Internally via **containers** service name and port, i.e. http://web:5000, but we wouldn't be able to access this. We can via the published ports.

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

- If you wanted to be more precise around Redis been up & ready, how would you implement this? (hint: [health & readiness](https://docs.docker.com/engine/reference/builder/#healthcheck))

## Launching and tearing down your compose stack

To launch your stack: `docker compose up`

If you receive a `no configuration file provided: not found` this is most likely due to non-standard naming convention followed. Use the `-f` flag _after_ compose and _before_ the subcommand e.g. `up`.

you should be able to see the docker file being built and also redis image. If we goto the website `http://localhost:8080`, we should now be able to see our counter increment with every page refresh.

To tear down our stack, we simply issue the command `docker compose down`, note if we want to remove volumes and network adapters we would also on the down command need to append `-v` or `--volumes`.

We can also list multiple compose stacks that are running via: `docker compose ls`

## Should you need to (re)build

Typical use case maybe needed only if there are changes on Dockerfiles. Following commands will assist with building images before starting containers

Build All:

```sh
docker compose up --build
```

or, build specific compose service:

```sh
docker-compose up --build <service name>
```

> NOTE: Above commands uses cache images if it is exist. Using `docker-compose build --no-cache` never uses cache fully rebuilding all layers.

or if you don't want to run but see the services build giving simpler plain output for each instruction in the `Dockerfile`:

```sh
docker compose build --no-cache --progress=plain
```

## Persisting Redis data

Reviewing the [redis docker page](https://hub.docker.com/_/redis) we have various methods to persist the data which is made available in the running container at `/data`.

We can use a docker volume or a DB like Postgres, etc. From our previous working knowledge and referring to the compose documentation on [volume usage](https://docs.docker.com/storage/volumes/#use-a-volume-with-docker-compose), can you configure the `redis` service to use a volume

> NOTE: As a stretch goal, you could configure another service called `db` to run a Postgres image which consumes the `redis` service data.

## loading .env for custom environment variables

It can be quite useful when testing to use `.env` files to change how your project is configured i.e. simulate production. This can be loaded in at your parent directory, for more configuration options refer to the [docs](https://docs.docker.com/compose/environment-variables/#the-env-file).

## Overriding the CMD command

It can be useful when running compose to be able to change the arg, you may need to always run things slightly different on your local version when developing. With compose this is simple to do. Explore by changing the command that is run inside the dockerfile using the following on your flask service:

```yaml
command: /bin/bash -c "echo hellooooo world"
```

### Question

- What has happened to the original command?
- When might this be useful in your developer workflow?

## secure way to add secrets during build

Inspecting your docker file, like we have done previously (e.g. `docker inspect` & `docker history`) to see the layers in the previous exercise, if we were to use environment variable, you would quickly see that this is persisted to the image. This means anyone with access to the image, could quickly see potential sensitive data.

There is a way to mitigate through the usage of the [`--secret` build parameter](https://docs.docker.com/engine/reference/commandline/buildx_build/#secret). We can test secret mounting via a text file. This secret will only live on until the usage of the command it is mounted with, then voilà no longer.

Below is an example I have used in Node docker image which contained a sensitive token to access a private repo:

build time secret use `--mount` parameter within a `Dockerfile` `RUN` command`:

```dockerfile
RUN --mount=type=secret,mode=0644,id=npmrc,target=/usr/src/app/.npmrc npm ci --only-production
```

> NOTE: default location for secrets mounted without a target would be `/run/secrets/<secret id>`

Above you can see various additional configurations such as:

- `mode` to set read, write, execute permissions of the secret
- `type` this can be `secret` (_as demonstrated_), or [`ssh`](https://docs.docker.com/develop/develop-images/build_enhancements/#using-ssh-to-access-private-data-in-builds)
- `id` is the identifier to pass into the `docker build --secret`, this id is associated with the `RUN --mount` identifier to use in the Dockerfile
- `target` is the destination of the output of the secret

Using the secret we can run the docker cli `build` command with `id` of the secret (_i.e. to match with our secret mount_) and use a path for `src` from the working directory build context:

```sh
docker build  . -t version-tag  --secret id=npmrc,src=.npmrc
```

## Adding secure secrets to build via compose

> Note: Only recently [supported](https://github.com/compose-spec/compose-spec/pull/238) as of 11/04/2022 [documentation](https://docs.docker.com/compose/compose-file/build/#secrets) elaborates on more complex use cases/config.

New yaml configuration block at the root level after the services to configure the `secrets` section. This can be file or environment variables:

```yaml
secrets:
  npmrc:
    file: .npmrc #path relative to the docker context
  topsecretkey:
    environment: TOP_SECRET # in shell env or passed directly via build
  #... many more here
```

> NOTE: There is a difference between secret usage for run time and build time, it's important to keep that in mind.

We now need to add to our flask service the reference, the useful nature of this is re-use too if that is a use case of your own:

```yaml
flask:
  build:
    context: .
    secrets:
      - npmrc # read-only by default
```

> NOTE: Secrets are optional by default, you will not receive an error until trying to access the secret. Mark the secret as `required` for a informative error in this regard

### Questions

- testing the above in your Dockerfile and re-building, can you access the secret file whilst your container is running? (hint: `docker exec it <id or name> /bin/bash`)
- What use cases do you think this would be useful for?
- How would we think about run time secrets, what could we do for this scenario?

## Security aspects to be mindful of when creating images

### Scanning

Security scanning is something that is vital in every aspect of your SDLC! This should be a first class citizen in your commit to production workflows, ensuring/mitigating security vulnerabilities that could be potentially be exploited effecting the business and customers. As developers and operational usage of sec tooling, we need fast feedback and be able to be able control how we deal with the thread landscape, so the tooling choice needs to offer configuration to control the risk & acceptance, etc. There are many 3rd party tools out there to help in this regard.

Controlling how we deal with a vulnerability (vuln) may be determined on multiple factors. A vuln may exist in a package, however the way it's used at your company may not effect you, this is something you would have to evaluate, tooling can help in this regard for controlling mitigating factors. A vuln could be high risk (e.g. a big threat LOG4J vuln) and require immediate attention, this is why automated and scheduled scanning is extremely important! Tooling can create a way of controlling company wide, and per-repo basis how a threat should be treated. This process can automated and controlled to terminate relevant containers with updated versions on a rolling basis.

> NOTE: Refer to the top-level repo [README](../README.md) for extra notes to enhance your docker knowledge further on security, best practices, orchestration.

### Scanners ability to pickup vulnerabilities

One thing that you may see throughout the containerisation world when building images are dynamic scripts in Dockerfile's to pull in resources, e.g. install different versions of software, build scripts, etc... Why potentially may this be a _"bad practice"_?

When we think of modern security scanning processes and tooling in the ecosystem, automated security scanners are not able to always detect these means and outcomes of scripts... (_NOTE: I'm sure their are very bright people working on this specific issue!_). They are typically looking for packages through known build tooling e.g. `rpm`, `apt`, `apk`, language specific tooling `pip`, `maven/gradle`, etc, etc. Otherwise, we are potentially working around what the tooling is looking for leading to unknown vulnerabilities present.

Until the tooling evolves enough to combat the potential risks of out-of-date versioning, 0-days, known vulnerabilities, and have an advanced understanding of building from source; avoiding custom clever scripts for dynamic installs, etc is advised to assist in security scanning tooling to inform you on potential vulnerabilities.

## Cleanup

To stop and remove all the running and exited containers & volumes and perform a cleanup of docker cache

```sh
docker ps -a -q | xargs docker rm -f && docker system prune -a --force
```
