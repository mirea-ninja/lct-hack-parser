.PHONY: lint
format:
	isort --force-single-line-imports app
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
	black app
	isort app

.PHONY: connect
connect:
	docker-compose exec parser bash

.DEFAULT_GOAL :=
