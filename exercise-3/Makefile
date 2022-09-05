test:
	poetry install
	poetry run pytest

shell:
	docker run -it -v $(PWD):/app my-app:devel /bin/bash

build:
	docker build -f Dockerfile.example -t my-app:devel .

run:
	docker run -p 8080:80 -d my-app:devel