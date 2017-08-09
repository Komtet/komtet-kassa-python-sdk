.PHONY: all buildout tests publish

BOOTSTRAP_BUILDOUT = "https://bootstrap.pypa.io/bootstrap-buildout.py"

all:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

buildout: ## Setup development environment
	@rm bootstrap.py -f
	@rm buildout -rf
	@wget $(BOOTSTRAP_BUILDOUT) -O bootstrap.py
	@for v in 2 3; do \
		mkdir -p buildout/$$v;\
		python$$v bootstrap.py -c py$$v.cfg;\
		buildout/$$v/bin/buildout -c py$$v.cfg;\
		rm .installed.cfg;\
	done
	@rm bootstrap.py

tests:    ## Run tests
	@for v in `ls buildout`; do \
		echo Python $$v;\
		buildout/$$v/bin/coverage run --source src setup.py test -q && buildout/$$v/bin/coverage report -m;\
		echo;\
	done
	@rm .coverage

publish:  ## Upload package to PyPI
	@python setup.py sdist upload
