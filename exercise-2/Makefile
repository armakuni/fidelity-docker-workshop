test:
	poetry install
	poetry run pytest

shell:
	docker run -it -v $(PWD):/app:ro my-poetry:devel /bin/bash