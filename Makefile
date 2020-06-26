lint:
	flake8 snflambda
	flake8 test

test: clean-pyc
	pytest --cov=snflambda
	
clean-pyc:
	rm -f *.pyc
	rm -f snflambda/*.pyc
	rm -f test/*.pyc

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean: clean-pyc clean-build

build: clean lint test
	python3 setup.py sdist bdist_wheel
