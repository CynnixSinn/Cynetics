.PHONY: help install test lint format clean docker-build run

help:
	@echo 'Cynetics - Make Commands'
	@echo ''
	@echo 'Usage:'
	@echo '  make install       Install all dependencies'
	@echo '  make test          Run tests'
	@echo '  make lint          Lint code'
	@echo '  make format        Format code'
	@echo '  make clean         Clean build artifacts'
	@echo '  make docker-build  Build Docker image'
	@echo '  make run           Run example project'

install:
	pip install -r requirements.txt
	npm install -g @modelcontextprotocol/server-filesystem \
		@modelcontextprotocol/server-git \
		@modelcontextprotocol/server-shell \
		@modelcontextprotocol/server-memory

test:
	pytest tests/ -v --cov=. --cov-report=html

lint:
	pylint cynetics.py
	ruff check .

format:
	black .
	ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .coverage htmlcov/ dist/ build/ *.egg-info

docker-build:
	docker build -t cynetics:latest .

run:
	python cynetics.py --description "Build a simple REST API for managing tasks"

init:
	python cynetics.py --init
	cp .env.example .env
	@echo "✓ Initialized! Edit .env with your API keys"
