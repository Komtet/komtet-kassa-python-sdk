.PHONY: help all build test test_legacy test_all create_eggs
.DEFAULT_GOAL := help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

all:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:		## Build containeras
	@docker-compose build --no-cache

test_legacy:	## Run tests fof python 2.7
	@docker-compose run python2 bash -c 'coverage run --source src setup.py test && coverage report -m'

test:		## Run tests for python 3.6
	@docker-compose run python3 bash -c 'coverage run --source src setup.py test && coverage report -m'

test_all:  	## Run all tests
	@make test_legacy && make test

publish:	## Upload package to PyPI
	@python3 setup.py sdist upload

eggs:		## Собрать яйца
	@docker-compose run python2 bash -c 'python setup.py bdist_egg'
	@docker-compose run python3 bash -c 'python setup.py bdist_egg'
	@sudo chown $$USER:$$USER -R ./dist

