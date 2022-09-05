test:
	poetry install
	poetry run pytest

shell:
	docker run --rm -it -v $(PWD):/app my-poetry:devel /bin/bash

build:
	docker build -f Dockerfile.example -t my-poetry:devel .