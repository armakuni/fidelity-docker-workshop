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

## Pull a third party image

[Nginx docker image](https://hub.docker.com/_/nginx/)

```sh
docker pull nginx:latest
docker images
```

- image IDs

## Run the third party image foreground

```sh
docker run -p 8080:80 nginx
```

You can hit this in the browser.

### Questions

- Why can't I use a low-numbered port, e.g. `-p 80:80`?

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

## Mount a volume with content

```sh
docker run --name my-nginx -p 8080:80 -v /some/content:/usr/share/nginx/html:ro -d --rm nginx
curl http://localhost:8080/
docker kill my-nginx
```

see folder: [exercise-1/html](./html/)` for mounting html contents

### Questions

- What happens if you don't add the `:ro` suffix when mounting a volume? [Volume Docker Docs](https://docs.docker.com/storage/volumes/)

## Run an interactive shell

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
