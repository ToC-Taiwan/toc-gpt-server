PYTHON=$(shell which python3)
PIP=$(shell which pip3)
PWD=$(shell pwd)

run: check ### run
	@$(PYTHON) -BO ./src/main.py
.PHONY: run

lint: check ### lint
	@mypy --check-untyped-defs --config-file=./mypy.ini ./src
.PHONY: lint

install: check ### install dependencies
	@$(PIP) install --no-warn-script-location --no-cache-dir -r requirements.txt
	@$(PIP) install --no-warn-script-location --no-cache-dir mypy-protobuf pylint-protobuf mypy pylint
	@mypy --install-types --check-untyped-defs --non-interactive ./src
.PHONY: install

update: check ### update dependencies
	@./scripts/update_dependency.sh $(PIP)
	@./scripts/install_dev_dependency.sh $(PIP)
	@./scripts/compile-proto.sh $(PYTHON)
.PHONY: update

proto: check ### compile proto
	@./scripts/compile-proto.sh $(PYTHON)
.PHONY: proto

venv: ## create virtual environment
ifneq ($(shell $(PYTHON) --version | awk '{print $$2}'),3.10.11)
	$(error "Please use python 3.10.11")
endif
	@rm -rf venv
	@$(PYTHON) -m venv venv
.PHONY: venv

check: ## check environment
ifneq ($(PYTHON),$(PWD)/venv/bin/python3)
	$(error "Please run 'make venv' first")
endif
	@echo "Venv pyython version: $(shell $(PYTHON) --version | awk '{print $$2}')"
	@echo "Python path: $(PYTHON)"
.PHONY: check

help: ## display this help screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help
