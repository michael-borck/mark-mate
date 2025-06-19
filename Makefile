.PHONY: help install install-dev test lint format typecheck clean docs docs-serve setup
.DEFAULT_GOAL := help

PYTHON := python3
UV := uv
VENV := .venv
PYTHON_VENV := $(VENV)/bin/python
PIP_VENV := $(VENV)/bin/pip

help: ## Show this help message
	@echo "MarkMate Development Commands"
	@echo "============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Set up development environment with uv
	@echo "Setting up development environment..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "Using uv for fast dependency management..."; \
		uv venv $(VENV) --python $(PYTHON); \
		uv pip install -e ".[dev,docs]"; \
	else \
		echo "uv not found, falling back to venv + pip..."; \
		$(PYTHON) -m venv $(VENV); \
		$(PIP_VENV) install --upgrade pip; \
		$(PIP_VENV) install -e ".[dev,docs]"; \
	fi
	@echo "✓ Development environment ready!"
	@echo "Activate with: source $(VENV)/bin/activate"

install: $(VENV) ## Install package in development mode
	$(PIP_VENV) install -e .

install-dev: $(VENV) ## Install package with development dependencies
	$(PIP_VENV) install -e ".[dev,docs]"

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(PIP_VENV) install --upgrade pip

test: ## Run tests with pytest
	$(PYTHON_VENV) -m pytest tests/ -v

test-cov: ## Run tests with coverage report
	$(PYTHON_VENV) -m pytest tests/ --cov=mark_mate --cov-report=html --cov-report=term-missing

lint: ## Run ruff linter
	$(PYTHON_VENV) -m ruff check src/ tests/

lint-fix: ## Run ruff linter with auto-fix
	$(PYTHON_VENV) -m ruff check --fix src/ tests/

format: ## Format code with ruff
	$(PYTHON_VENV) -m ruff format src/ tests/

format-check: ## Check code formatting
	$(PYTHON_VENV) -m ruff format --check src/ tests/

typecheck: ## Run type checking with basedpyright
	$(PYTHON_VENV) -m basedpyright src/

check-all: format-check lint typecheck test ## Run all checks (format, lint, typecheck, test)

docs: ## Build documentation
	$(PYTHON_VENV) -m mkdocs build

docs-serve: ## Serve documentation locally
	$(PYTHON_VENV) -m mkdocs serve

docs-deploy: ## Deploy documentation to GitHub Pages
	$(PYTHON_VENV) -m mkdocs gh-deploy

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-all: clean ## Clean everything including virtual environment
	rm -rf $(VENV)

build: ## Build the package
	$(PYTHON_VENV) -m build

publish-test: build ## Publish to PyPI test
	$(PYTHON_VENV) -m twine upload --repository testpypi dist/*

publish: build ## Publish to PyPI
	$(PYTHON_VENV) -m twine upload dist/*

install-uv: ## Install uv package manager
	@echo "Installing uv..."
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "✓ uv installed. Restart your shell or run: source ~/.cargo/env"