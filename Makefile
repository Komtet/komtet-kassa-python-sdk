.PHONY: all build test test_legacy test_all create_eggs

BOOTSTRAP_BUILDOUT = "https://bootstrap.pypa.io/bootstrap-buildout.py"

all:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:
	@docker-compose build --no-cache

test_legacy:
	@docker-compose run python2 bash -c 'coverage run --source src setup.py test && coverage report -m'

test:
	@docker-compose run python3 bash -c 'coverage run --source src setup.py test && coverage report -m'

test_all:  test_legacy test

publish:  ## Upload package to PyPI
	@python3 setup.py sdist upload

eggs:
	@docker-compose run python2 bash -c 'python setup.py bdist_egg'
	@docker-compose run python3 bash -c 'python setup.py bdist_egg'
	@sudo chown $$USER:$$USER -R ./dist
	@sudo chown $$USER:$$USER -R ./src
