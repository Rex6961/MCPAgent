.PHONY: install test lint format run clean

install:
	poetry install

test:
	poetry run pytest -v

lint:
	poetry run ruff check
	poetry run mypy src

format:
	poetry run ruff format

run:
	poetry run python -m src.mcp_agent.agent

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
