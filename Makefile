help:	## Show all Makefile targets.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

lint: ## Run linters: pre-commit (black, ruff, codespell) and mypy
	pre-commit install
	git ls-files | xargs pre-commit run --show-diff-on-failure --files

format: ## Run code autoformatters (ruff).
	pre-commit install
	git ls-files | xargs pre-commit run ruff-format --files

test:	## Run tests via pytest.
	pytest tests
