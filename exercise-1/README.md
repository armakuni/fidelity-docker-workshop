# Exercise 1 - basics

In this exercise, you will get use some basic Docker commands to download and run a simple web server.

## Master basic Docker commands

```sh
docker --help
docker images
docker ps
docker pull
docker run
```

> NOTE: You can run any docker command e.g. `run`, `pull`, etc with `--help`

## Commands ordering

The order of the command to execute on the CLI is always `docker` followed by the command e.g. `run` then the one or more command options e.g. `-p`

## Pull a third party image

[Nginx docker image](https://hub.docker.com/_/nginx/)

```sh
docker pull nginx:latest
docker images
```

## Run the third party image foreground

```sh
docker run -p 8080:80 nginx
```

You can now view the webpage in the browser.

## Run the third party image background

```sh
docker run --name my-nginx -p 8080:80 -d nginx
curl http://localhost:8080/
docker ps
docker kill my-nginx
docker rm my-nginx
```

### Questions

- If you forget to name your container, how can you kill it?
- Try `docker ps -a`, what do you see?
- There is another flag `--rm` that will auto-remove the container when you kill it

## How do we check our application logs?

If the application outputs to `STDOUT` and `STDERR` instead of a text file on a filesystem, then the following docker command will contain your output.

```sh
docker logs <ID or container name>
```

> NOTE: adding `-f` will follow the output streamed with any new updates, this can be useful for debugging and development purposes.

## Bind Mount a folder from your host machine to a container

Volumes are storage which is represented by the option: `-v` or `--volume`, there are 3 types of storage:

- [bind mounts](https://docs.docker.com/storage/bind-mounts/#start-a-container-with-a-bind-mount) (we demonstrate below)
- [docker volume](https://docs.docker.com/storage/volumes/#create-and-manage-volumes)
- [tmpfs](https://docs.docker.com/storage/tmpfs/).

The following is running the same image as we did previously, however with a **bind mount** using the `-v` volume command to mount across our HTML.

Bind Mount a file or directory from the host machine mounted inside a container at a specified path. The file or directory has to be referenced by its full path on the host machine. This is why we make use of the `pwd` CLI command from our `exercise-1` folder.

```sh
docker run --name my-nginx -p 8080:80 -v "$(pwd)/html":/usr/share/nginx/html:ro -d --rm nginx
curl http://localhost:8080/ # or open me in the browser too!
docker kill my-nginx
```

> NOTE: see folder: [exercise-1/html](./html/)` for mounting html contents

### Questions

- What happens if you don't add the `:ro` suffix when mounting a volume? [Docker Volume: Bind Mount Docs](https://docs.docker.com/storage/bind-mounts/#use-a-read-only-bind-mount)

## Run an interactive shell

The following additional args after the image name: `/bin/bash` is a command to run, this is in fact overriding the default behavior of how the Nginx container would run.

This following command allows us to run a bash shell typically how you would interact with your own CLI.

```sh
docker run -it nginx /bin/bash
```

### Questions

- Does anything persist between `docker run` commands?

## Hack into a running image

```sh
docker run --name my-nginx -p 8080:80 -v /some/content:/usr/share/nginx/html:ro -d --rm nginx
docker exec -it my-nginx /bin/bash
# now wander around the shell in the container
docker kill my-nginx
```

## Set environment variables

```sh
docker run -it -e FOO=bar nginx /bin/bash
```
