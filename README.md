# exchange-tests

Test automation framework for the exchange service.

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

## Install

```bash
uv sync
```

## Configuration

Settings are read from environment variables with the `EXCHANGE_TESTS_` prefix
or from a `.env` file in the project root. Environment variables take priority.

```bash
cp .env.example .env
```

Then edit `.env`. The `.env` file is git-ignored; never commit real secrets.

## Checks

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```
