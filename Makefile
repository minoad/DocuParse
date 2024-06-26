.PHONY: build
build:
	pip install -e .
	pre-commit install

.PHONY: docker_clean
docker_clean:
	docker image prune --all -f
	docker container prune -f
	docker volume prune -f --all
	cd .devcontainer && docker-compose down --rmi all --volumes --remove-orphans

.PHONY: mypy
mypy:
	mypy --ignore-missing-imports plat/

.PHONY: test
test:
	pytest test/

.PHONY: precommit
precommit:
	pre-commit run --all-files

.PHONY: coverage
coverage:  ## Run tests with coverage
	coverage erase
	coverage run -m pytest
	coverage report -m
	python -m pytest --cov=docuparse --cov-report=html tests/

.PHONY: lint
lint: pylint flake8 black mypy

.PHONY: pylint
pylint:
	pylint --max-line-length=120 plat/

.PHONY: flake8
flake8:
	flake8 --max-line-length=120 --ignore=E266,E402,F841,F401,E302,E305 .

.PHONY: checklist
checklist: lint typehint test

.PHONY: black
black:
	black -l 120 .

.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
