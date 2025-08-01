# PyPrompt - Makefile for build automation
# 
# Main targets:
#   make install     - Install package locally
#   make build       - Build distribution packages
#   make clean       - Clean build artifacts
#   make lint        - Run code linting
#   make format      - Format code
#   make validate    - Validate package
#   make publish     - Publish to PyPI
#   make help        - Show this help

.PHONY: help install install-dev build clean lint format validate test publish check-env

# Default target
.DEFAULT_GOAL := help

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)PyPrompt - Available Make Targets$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

install: ## Install package locally in development mode
	@echo "$(YELLOW)Installing pyprompt in development mode...$(RESET)"
	pip install --upgrade setuptools wheel
	pip install -e .
	@echo "$(GREEN)✓ Installation complete$(RESET)"

install-dev: ## Install package with development dependencies
	@echo "$(YELLOW)Installing pyprompt with development dependencies...$(RESET)"
	pip install -e ".[dev]"
	@echo "$(GREEN)✓ Development installation complete$(RESET)"

build: clean install-deps ## Build distribution packages
	@echo "$(YELLOW)Building distribution packages...$(RESET)"
	python -m pip install --upgrade build
	python -m build
	@echo "$(GREEN)✓ Build complete - packages in dist/$(RESET)"

clean: ## Clean build artifacts and cache files
	@echo "$(YELLOW)Cleaning build artifacts...$(RESET)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.orig" -delete
	find . -type f -name "*.rej" -delete
	@echo "$(GREEN)✓ Clean complete$(RESET)"

format: ## Format code with black and isort
	@echo "$(YELLOW)Formatting code...$(RESET)"
	python -m black pyprompt/
	python -m isort pyprompt/
	@echo "$(GREEN)✓ Code formatting complete$(RESET)"

lint: ## Run code linting with flake8 and mypy
	@echo "$(YELLOW)Running code linting...$(RESET)"
	python -m flake8 pyprompt/ --max-line-length=88 --extend-ignore=E203,W503,E501,D100,D200,D202,D205
	python -m mypy pyprompt/ --ignore-missing-imports
	@echo "$(GREEN)✓ Linting complete$(RESET)"

validate: lint install-deps ## Validate package configuration and build
	@echo "$(YELLOW)Validating package...$(RESET)"
	python -m pip install --upgrade setuptools wheel twine
	python setup.py check --strict --metadata
	@if [ -d "dist/" ]; then \
		python -m twine check dist/*; \
	else \
		echo "$(YELLOW)No dist/ directory found, running build first...$(RESET)"; \
		$(MAKE) build; \
		python -m twine check dist/*; \
	fi
	@echo "$(GREEN)✓ Package validation complete$(RESET)"

install-deps: ## Install required build dependencies
	@echo "$(YELLOW)Installing build dependencies...$(RESET)"
	python -m pip install --upgrade pip setuptools wheel build twine
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

test: ## Run tests (placeholder - tests not implemented yet)
	@echo "$(YELLOW)Running tests...$(RESET)"
	@echo "$(BLUE)Note: Tests not implemented yet$(RESET)"
	@echo "$(GREEN)✓ Test suite complete$(RESET)"

version-check: ## Check version consistency across files
	@echo "$(YELLOW)Checking version consistency...$(RESET)"
	@VERSION_INIT=$$(grep '^__version__ =' pyprompt/__init__.py | cut -d'"' -f2); \
	VERSION_PYPROJECT=$$(grep '^version' pyproject.toml | cut -d'"' -f2); \
	VERSION_SETUP=$$(grep 'version=' setup.py | cut -d'"' -f2); \
	if [ "$$VERSION_INIT" = "$$VERSION_PYPROJECT" ] && [ "$$VERSION_INIT" = "$$VERSION_SETUP" ]; then \
		echo "$(GREEN)✓ All versions match: $$VERSION_INIT$(RESET)"; \
	else \
		echo "$(RED)✗ Version mismatch:$(RESET)"; \
		echo "  __init__.py: $$VERSION_INIT"; \
		echo "  pyproject.toml: $$VERSION_PYPROJECT"; \
		echo "  setup.py: $$VERSION_SETUP"; \
		exit 1; \
	fi

check-env: ## Check environment setup
	@echo "$(YELLOW)Checking environment...$(RESET)"
	@python --version
	@echo "Python executable: $$(which python)"
	@if python -c "import openai" 2>/dev/null; then \
		echo "$(GREEN)✓ OpenAI package available$(RESET)"; \
	else \
		echo "$(RED)✗ OpenAI package not found$(RESET)"; \
	fi
	@if python -c "import pydantic" 2>/dev/null; then \
		echo "$(GREEN)✓ Pydantic package available$(RESET)"; \
	else \
		echo "$(RED)✗ Pydantic package not found$(RESET)"; \
	fi
	@if [ -n "$$OPENAI_API_KEY" ]; then \
		echo "$(GREEN)✓ OPENAI_API_KEY environment variable set$(RESET)"; \
	else \
		echo "$(YELLOW)⚠ OPENAI_API_KEY not set - will be required at runtime$(RESET)"; \
	fi

publish: validate ## Publish to PyPI (production)
	@echo "$(YELLOW)Publishing to PyPI...$(RESET)"
	@echo "$(RED)⚠ This will publish to production PyPI!$(RESET)"
	@read -p "Are you sure? (y/N) " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		if [ ! -d "dist/" ]; then \
			echo "$(YELLOW)No dist/ directory found, running build first...$(RESET)"; \
			$(MAKE) build; \
		fi; \
		python -m twine upload dist/*; \
		echo "$(GREEN)✓ Published to PyPI$(RESET)"; \
	else \
		echo "$(YELLOW)Publication cancelled$(RESET)"; \
	fi

deps-check: ## Check for outdated dependencies
	@echo "$(YELLOW)Checking for outdated dependencies...$(RESET)"
	pip list --outdated

deps-update: ## Update dependencies (use with caution)
	@echo "$(YELLOW)Updating dependencies...$(RESET)"
	pip install --upgrade openai pydantic

all: clean format lint validate build ## Run full pipeline: clean, format, lint, validate, build
	@echo "$(GREEN)✓ Full pipeline complete$(RESET)"

dev-setup: ## Set up development environment
	@echo "$(YELLOW)Setting up development environment...$(RESET)"
	pip install --upgrade pip
	$(MAKE) install-dev
	@echo "$(GREEN)✓ Development environment ready$(RESET)"
	@echo "$(BLUE)Don't forget to set OPENAI_API_KEY environment variable$(RESET)"

# Print variables for debugging
debug: ## Show debug information
	@echo "$(BLUE)Debug Information:$(RESET)"
	@echo "Python: $$(python --version)"
	@echo "Pip: $$(pip --version)"
	@echo "Working directory: $$(pwd)"
	@echo "Files in current directory:"
	@ls -la
	@if [ -f "pyprompt/__init__.py" ]; then \
		echo "Package version: $$(grep '__version__' pyprompt/__init__.py | cut -d'"' -f2)"; \
	fi 