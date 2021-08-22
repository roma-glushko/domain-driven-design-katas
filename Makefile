flake:
	flake8 ./src ./tests

isort:
	isort ./src ./tests

black:
	black ./src ./tests

mypy:
	mypy ./src ./tests

lint:
	make isort && make black && make flake && make mypy