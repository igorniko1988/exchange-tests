# exchange-tests

API and UI test automation framework for the exchange service (pytest, requests, Playwright).

## Requirements
- Python 3.13, uv
- Running stand (repo `igorniko1988/tests`): `cd ~/Downloads/tests && docker compose up -d db exchange price-feed`, API on http://localhost:8080

## Install
uv sync

## Run tests
```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```