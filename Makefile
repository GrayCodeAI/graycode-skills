.PHONY: boundary-guard lint format registry-check validate test help

boundary-guard: ## Fail if the skills repo references support engines or Hawk private packages
	bash ./scripts/check-consumer-boundaries.sh

lint: ## Run Ruff over all repository Python code
	ruff check .

format: ## Format all repository Python code
	ruff format .

registry-check: ## Fail if registry.json is stale
	python3 tools/update_registry.py --check

validate: registry-check ## Validate all skills in the registry
	python3 tools/validate_skill.py --all --warning-budget tools/validation_warning_budget.json

pytest: ## Run pytest unit tests
	python3 -m pytest tests/ -v

test: boundary-guard lint validate pytest ## Run all checks

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: hooks
hooks:
	git config core.hooksPath .githooks
