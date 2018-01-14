compile: main.py
	python -m compileall main.py

run: compile
	python main.pyc
