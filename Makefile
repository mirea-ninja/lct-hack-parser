.PHONY: lint
format:
	isort --recursive  --force-single-line-imports --apply app
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
	black app
	isort --recursive --apply app

.PHONY: connect
connect:
	docker-compose exec backend bash

.DEFAULT_GOAL :=
