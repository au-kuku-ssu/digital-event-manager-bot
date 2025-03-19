PHONY: *

setup:
ifeq ($(OS),Windows_NT)
	powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
else
	curl -LsSf https://astral.sh/uv/install.sh | sh
endif

install:
	uv sync
	uv run pre-commit install
run:
	uv run bot/main.py
