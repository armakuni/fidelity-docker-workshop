test:
	poetry install
	poetry run pytest

shell:
	docker run -it -v $(PWD):/app my-app:devel /bin/bash

build:
	docker build -f Dockerfile.example -t my-app:devel .
	
build-compose:
	docker compose -f docker-compose-example.yml build --no-cache --progress=plain

run:
	docker run -p 8080:5000 -d my-app:devel