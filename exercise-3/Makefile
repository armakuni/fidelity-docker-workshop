test:
	poetry install
	poetry run pytest

shell:
	docker run -it my-app:devel sh

build:
	docker build -f Dockerfile.example -t my-app:devel .

build-debug:
	docker build -f Dockerfile.example -t my-app:devel . --progress plain --no-cache

run:
	docker run --rm -p 8080:5000 my-app:devel