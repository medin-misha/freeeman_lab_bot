# Backend

FastAPI backend проекта `freeeman_lab_bot`.

Сервис отвечает за:

- CRUD пользователей
- CRUD диагностик
- CRUD заявок `Core`
- загрузку и выдачу файлов через S3 / MinIO
- health endpoints
- публикацию событий в RabbitMQ

## Запуск

### Локально

```bash
cd backend
uv sync --frozen
uv run alembic upgrade head
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### В Docker Compose

```bash
docker compose up --build -d freeman-backend
```

В Docker backend стартует через `start_backend.py`, который ждёт доступности PostgreSQL, RabbitMQ и S3 / MinIO до запуска `uvicorn`.

## Переменные окружения

Backend читает переменные из `backend/.env`.

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `DATABASE` | да | строка подключения к PostgreSQL |
| `AWS_S3_ACCESS_KEY` | да | S3 / MinIO access key |
| `AWS_S3_SECRERT_KEY` | да | S3 / MinIO secret key |
| `AWS_S3_BUCKET_NAME` | да | bucket для файлов |
| `AWS_S3_ENDPOINT_URL` | да | endpoint S3 / MinIO |
| `RMQ_URL` | да | RabbitMQ URL |
| `RMQ_DIAGNOSTIC_REQUEST_QUEUE` | да | очередь новых диагностик |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь готовых результатов |
| `RMQ_NUCLEUS_APPLICATION_QUEUE` | нет | очередь заявок `Ядро` |

Важно:

- код ожидает именно `AWS_S3_SECRERT_KEY`
- опечатка в имени переменной является частью текущего контракта

## Миграции

Применить все миграции:

```bash
cd backend
uv run alembic upgrade head
```

Текущая ревизия:

```bash
uv run alembic current
```

Создать новую миграцию:

```bash
uv run alembic revision -m "description"
```

## HTTP endpoints

### Service

- `GET /live` — liveness probe
- `GET /ready` — readiness probe с проверкой БД, RabbitMQ и S3
- `GET /health` — подробный healthcheck
- `GET /metrics` — Prometheus metrics

### Users

- `POST /users`
- `GET /users`
- `GET /users/{id}`
- `PATCH /users/{id}`
- `POST /users/bulk`
- `DELETE /users/{id}`

### Files

- `POST /files/`
- `GET /files/`
- `GET /files/{file_id}`

### Diagnostics

- `POST /diagnostics`
- `GET /diagnostics`
- `GET /diagnostics/{id}`
- `PATCH /diagnostics/{id}`
- `DELETE /diagnostics/{id}`

### Core

- `GET /core`
- `GET /core/{id}`
- `POST /core/submit`
- `PATCH /core/{id}`
- `DELETE /core/{id}`

## События RabbitMQ

### Диагностика

- после `POST /diagnostics` backend публикует событие в `RMQ_DIAGNOSTIC_REQUEST_QUEUE`
- после `PATCH /diagnostics/{id}` с `result_file_id` backend публикует событие в `RMQ_DIAGNOSTIC_RESPONSE_QUEUE`

### Заявка в Ядро

- после `POST /core/submit` backend публикует событие в `RMQ_NUCLEUS_APPLICATION_QUEUE`

## Работа с файлами

- файлы сохраняются в S3 / MinIO
- лимит размера upload-файла в backend — `1000 МБ`
- выдача файла идёт через `GET /files/{file_id}`

## Проверка работоспособности

```bash
curl http://localhost:8000/live
curl http://localhost:8000/ready
curl http://localhost:8000/health
```

Пример `/live`:

```json
{"status":"ok","service":"backend"}
```

Если зависимости доступны, `/ready` возвращает `200 OK` и:

```json
{"status":"ok"}
```

Пример `/health`:

```json
{
  "status": "ok",
  "checks": {
    "backend": {"status": "ok"},
    "database": {"status": "ok"},
    "rmq": {"status": "ok"},
    "storage": {"status": "ok"}
  }
}
```

Если PostgreSQL, RabbitMQ или S3 / MinIO недоступны, `/ready` и `/health` вернут `503`.

## Структура

- `backend/main.py` — FastAPI app и health routes
- `backend/start_backend.py` — startup wrapper для Docker
- `backend/api/` — HTTP routers
- `backend/core/models/` — SQLAlchemy models
- `backend/service/files/` — работа с файлами
- `backend/service/diagnostic/` — публикация событий диагностики
- `backend/service/core/` — публикация событий `Ядро`

Логи:

```bash
docker compose logs -f freeman-backend
```
