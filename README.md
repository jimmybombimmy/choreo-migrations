# Choreo - Database Migrations

This repo creates database migrations for the Choreo app. This allows a user to easily spin up the required Postgres tables to run the app.

## Pre-requisites

- Postgres DB up, running and reachable with username and password
- Python v3.14 installed
- uv installed

## Setup

### 1. UV Setup

Run the following commands:

```bash
# Create venv folder
uv venv

# Enter virtual environment
source .venv/bin/activate

# Install packages
uv sync
```

### 2. Configure Environment Variables

Using the env vars from `env.example`, create a `.env` file at the project root with the following variables matching your Postgres DB setup:

```
POSTGRES_DB=choreo
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
```

### 3. Run Database Migrations

Easy peasy

```bash
alembic upgrade head
```

Further docs on upgrading and downgrading can be found here: https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration
