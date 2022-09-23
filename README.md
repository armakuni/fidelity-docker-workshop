# fidelity-docker-workshop

## How to use this repo

- Please open this repo in VSCode as a workspace project i.e. `File` -> `Open Workspace from File` -> Select Workspace file named `multi-root.code-workspace`
- Please refer to exercise README's
- Workshop Orchestrator: [Workshop Brief](containerisation_workshop.pdf)

### Non-docker usage

- When opening a terminal due to the nature of Python's need for virtual envs, please right click exercise folder and `open in integrated terminal`. This will do the work of placing you in the correct working directory.
- You will need to install via Poetry, this will setup your virtual environment and download the dependencies.
- Going forward selecting `open in integrated terminal` will automatically activate your virtual env, or manually via `poetry shell`.
  > NOTE: Watch out for mounting local virtual envs into your image builds

## How to install Docker

[Official Install Instructions](https://docs.docker.com/engine/install/) for Docker Desktop installation on Mac, Windows, Linux, current version of writing `Docker Desktop 4.12.0 (85629)`

> NOTE: Windows specific users may find installation via WSL 2 a enhanced developer experience: [wsl 2 docker docs](https://docs.docker.com/desktop/windows/wsl/)

## 20,000 foot concepts

- Docker
- What is an image?
- What is a container?
- What is Docker Hub?
- What is Fidelity's equivalent to Docker Hub?
- What is compose and how we can run multiple connected services?
- What are some best practices to follow i.e. production usage, security, layering, commands, etc?

## Exercises

### [Exercise 1 - basics](./exercise-1/README.md)

### [Exercise 2 - build your own image](./exercise-2/README.md)

### [Exercise 3 - packaging an app for production](./exercise-3/README.md)

### [Exercise 4 - docker compose and other concepts](./exercise-4/README.md)

### [Exercise 5 - Podman vs Docker Summary](./exercise-5/README.md)

### Exercise 6 - craving more docker knowledge?

- Security scanning tooling: [`docker scan`](https://docs.docker.com/engine/scan/) and 3rd party tools e.g. Synk, Aquasec, etc
- Continuous integration and continuous deployment with docker
- [Container orchestration](https://docs.docker.com/get-started/orchestration/)
- Docker & language specific optimisations
- [Docker advised best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi Platform builds to support different architectures](https://www.docker.com/blog/multi-platform-docker-builds/) e.g. `linux/arm/v7`, `linux/amd64`, `linux/arm64`
- [Linux Foundation - Developing Secure Software](https://training.linuxfoundation.org/training/developing-secure-software-lfd121/)

## Doing this in Fidelity

- Security concerns
- Scanning
- AWS elastic container registry
- Available core images
