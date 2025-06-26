# crypto-dashboard-backend

## Phase 1 — Project Setup

Initialized the project with FastAPI core structure.
Added Docker support for local development and environment configs.
Included a health check endpoint `/health`.
Set up `.env`, `.gitignore`, and initial formatting tools.

## Phase 2 — Auth & User Management

Integrated OAuth2 login with Google using Authlib.
Generated JWT tokens for user sessions.
Created `/auth/login`, `/auth/callback`, and `/auth/me` routes.
Stored basic user data in PostgreSQL.
Used cookies to pass access tokens securely.

## Phase 3 — Market Data API

Connected to Binance WebSocket API for live price ticks.
Stored tick data asynchronously in MongoDB using Motor.
Created REST endpoint `/prices/{symbol}` to query recent prices.
Built WebSocket endpoint `/ws/prices/{symbol}` for live price updates.

## Phase 4 — Watchlists & Portfolios

Created PostgreSQL models for user watchlists, trades, and virtual portfolios.
Enabled users to simulate fake trades via `/trade`.
Calculated total holdings based on trade history.
Exposed watchlist and portfolio routes: `/watchlist`, `/portfolio`.

## Phase 5 — Leaderboard System

Calculated user profit based on trade history.
Stored and updated leaderboard rankings in PostgreSQL.
Built `/leaderboard` endpoint and live updates with `/ws/leaderboard`.
Simulated Kafka-style messaging between trading and leaderboard modules.

## Phase 6 — Background Jobs

Created background jobs to sync top coins and clean old tick data.
Used Celery + Redis for async task execution.
Scheduled tasks to run hourly and daily as needed.
Prepared for Airflow or DAG-based workflows for complex pipelines.

## Phase 7 — DevOps & CI/CD

Added Docker services for MongoDB and PostgreSQL.
Created a `.env` file and used a `Makefile` for common tasks.
Set up GitHub Actions to run tests on every push or PR.
Enabled local dev environment with `docker-compose up`.
