.ONESHELL:

all: 
	python3 -m venv venv;
	. ./venv/bin/activate;
	pip install -r requirements.txt
	python setup.py build_ext --inplace;


test: test.py
	python3 test.py