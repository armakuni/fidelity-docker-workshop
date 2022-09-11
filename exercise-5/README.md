# Exercise 5 - Podman vs Docker Summary

## What is Podman?

[Podman](https://docs.podman.io/en/latest/index.html) is a competing container engine to Docker. Both have the same operational usages e.g. build, run, deploy, etc using [Open Containers Initiative](https://opencontainers.org/) (OCI).

## Why Podman instead?

As kubernetes is one of the major if not the way typically to do container orchestration at scale, podman has had a deep integration and making working in this ecosystem simpler through generating kubernetes configuration from your containers, running mock kubernetes workloads via CLI commands locally.

Redhat the people behind `podman` tool, do in fact have their own flavour of kubernetes which is called _Open Shift_. They have designed part of the tooling to integrate and make the developer experience user friendly.

## Podman vs Docker key facts

- Podman runs as a regular user & allows for non-root privileges for containers by default
- Docker can be run in 'rootless' mode at a detriment to features and more configuration
- Docker run on Client Server with daemon architecture (runs as root by default)
- Podman uses a single-process architecture (avoid the security issues related to the multi-process architecture, i.e. sharing PID namespace with all other containers)
- Podman 1-1 support with docker CLI commands and operations (e.g. performing: `docker build` vs `podman build`) ... has a few extras built in with the kubernetes ecosystem in mind
- Podman supports docker compose in part as of v4.1 2022 (no support for Buildkit specifics as of writing) and is not deemed top priority over continued Kubernetes integrations. (see: [The future of Podman and Compose](https://www.redhat.com/sysadmin/podman-compose-docker-compose))
- Podman has it's own Podman Compose community based project, no direct affiliation, better integrated for podman usage, but no integration with Docker's Compose
- Podman uses [buildah](https://github.com/containers/buildah/blob/main/docs/tutorials/01-intro.md) to build container images compliant with the Open Container Initiative

> NOTE: This is a changing landscape, correct as of September 2022

## Get started !

[Podman install & setup instructions](https://podman.io/getting-started/installation) there's also an optional equivalent docker-like desktop UI called [Podman Desktop](https://podman-desktop.io/downloads).

Now perform the same docker cli commands you've learned!

Typical 3 steps to get going on the mac:

```sh
brew install podman
podman machine init
podman machine start
```
