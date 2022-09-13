install:
	poetry install

shell:
	docker run --rm -it -v $(PWD):/app my-flask-compose-app:devel /bin/bash

build:
	docker build -t my-flask-compose-app:devel .

build-compose:
	docker compose -f docker-compose-example.yml build --no-cache --progress=plain