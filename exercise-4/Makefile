install:
	poetry install

shell:
	docker run --rm -it -v $(PWD):/app my-flask-compose-app:devel /bin/bash

build:
	docker build -t my-flask-compose-app:devel .