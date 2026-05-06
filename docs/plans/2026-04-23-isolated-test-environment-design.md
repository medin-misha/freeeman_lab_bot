# Isolated Test Environment Design

Date: 2026-04-23

## Goal

Make the default project environment fully test-only and self-contained. The
main `docker-compose.yml` must not depend on production-like external
PostgreSQL or RabbitMQ services, and it must not contain real Telegram or
Grafana credentials.

## Chosen Approach

Use the existing `docker-compose.yml` as the test stack by default.

Alternatives considered:

- Keep the current compose and add `docker-compose.test.yml`: safer for an
  existing deployment, but easy to run incorrectly.
- Add compose profiles for `test` and `external`: flexible, but too complex for
  a project that needs one unambiguous test mode.

## Architecture

The compose stack provides all infrastructure needed for local/test runs:

- `postgres` for the backend database.
- `rabbitmq` for backend, user bot, and admin bot queues.
- `freeman-minio` for S3-compatible storage.
- optional `telegram-bot-api` for local Telegram Bot API access in Docker.
- `freeman-backend`, `freeman-bot`, `freeman-admin-bot`, `freeman-mini-app`,
  and `nginx` as application services.

All inter-service URLs use Docker DNS service names, not host-local or external
addresses.

## Configuration

Test defaults:

- `DATABASE=postgresql+asyncpg://postgres:postgres@postgres:5432/freeman_test`
- `RMQ_URL=amqp://guest:guest@rabbitmq:5672/`
- `AWS_S3_ENDPOINT_URL=http://freeman-minio:9000`
- `API_URL=http://freeman-backend:8000`
- `TELEGRAM_BOT_API_URL=https://api.telegram.org`
- `VITE_API_URL=/api`

`nginx` exposes `/api/` and proxies it to `freeman-backend:8000`, so the mini
app can call the backend through the same origin.

## Safety Rules

- Do not hardcode real Telegram API ID/hash in compose.
- Do not hardcode real bot tokens or Grafana Telegram alert tokens.
- Keep real local `.env` files ignored by git.
- Keep committed examples safe and clearly test-oriented.

## Verification

- `docker compose config` must render successfully.
- Repository search must not find the previously hardcoded Telegram API ID/hash.
- The mini app must use `VITE_API_URL`, not `VITE_WEBHOOK_URL`.
