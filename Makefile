.DEFAULT_GOAL := help
export PYTHONDEVMODE = 1

.PHONY: dev
dev:  ## Install development requirements
	python3 -m pip install -r requirements.txt

export PYTHONDEVMODE = 1

.PHONY: fix
fix:  ## Fix code formatting, linting and sorting imports
	python3 -m pre_commit run --all-files

.PHONY: help
help:
	@echo "[Help] Makefile list commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: precommit_update
precommit_update:  ## Update pre_commit
	python3 -m pre_commit autoupdate

.PHONY: run
run:  ## Run demo
	python3 -m core.__init__ --map $(map)
