.PHONY: help install test lint format type-check clean dev setup

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Run the setup script
	./setup.sh

install: ## Install dependencies
	uv pip install -e ".[dev]"
	pip install pocketflow

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=claude_pocketflow_template --cov-report=html --cov-report=term

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .

fix: ## Fix linting issues
	uv run ruff check . --fix
	uv run ruff format .

type-check: ## Run type checking
	uv run pyright

check: lint type-check ## Run all checks

dev: ## Run all development checks
	make format
	make check
	make test

clean: ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

.env: ## Create .env file from example
	cp .env.example .env
	@echo "Created .env file. Please update with your API keys."
