# Backend

FastAPI backend для проекта `freeeman_lab_bot`.

Сервис отвечает за:

- CRUD пользователей
- CRUD диагностик
- загрузку и выдачу файлов
- публикацию событий в RabbitMQ
- работу с S3 / MinIO

## Запуск

### Локально

```bash
cd backend
uv sync --frozen
uv run alembic upgrade head
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### В Docker Compose

Из корня репозитория:

```bash
docker compose up --build -d freeman-backend
```

## Переменные окружения

Backend читает переменные из `backend/.env`.

Точные имена:

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `DATABASE` | да | строка подключения к PostgreSQL |
| `AWS_S3_ACCESS_KEY` | да | S3 / MinIO access key |
| `AWS_S3_SECRERT_KEY` | да | S3 / MinIO secret key |
| `AWS_S3_BUCKET_NAME` | да | bucket для хранения файлов |
| `AWS_S3_ENDPOINT_URL` | да | endpoint S3 / MinIO |
| `RMQ_URL` | да | RabbitMQ URL |
| `RMQ_DIAGNOSTIC_REQUEST_QUEUE` | да | очередь новых диагностик |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь готовых результатов |

Важно:

- код ожидает переменную `AWS_S3_SECRERT_KEY`
- в названии есть опечатка, и использовать нужно именно её

Пример для локального запуска:

```env
DATABASE=postgresql+asyncpg://postgres:postgres@localhost:5432/freeman
AWS_S3_ACCESS_KEY=admin
AWS_S3_SECRERT_KEY=supersecretpassword
AWS_S3_BUCKET_NAME=freeman-bucket
AWS_S3_ENDPOINT_URL=http://localhost:9000
RMQ_URL=amqp://guest:guest@localhost:5672/
RMQ_DIAGNOSTIC_REQUEST_QUEUE=diagnostic_request
RMQ_DIAGNOSTIC_RESPONSE_QUEUE=diagnostic_response
```

## Миграции

Применить все миграции:

```bash
cd backend
uv run alembic upgrade head
```

Посмотреть текущую ревизию:

```bash
uv run alembic current
```

Создать новую миграцию:

```bash
uv run alembic revision -m "description"
```

## API

Основные endpoints:

- `GET /health` — healthcheck
- `POST /users` — создать пользователя
- `GET /users` — получить пользователей
- `POST /files/` — загрузить файл
- `GET /files/{file_id}` — скачать файл
- `POST /diagnostics` — создать диагностику
- `GET /diagnostics/{id}` — получить диагностику
- `PATCH /diagnostics/{id}` — обновить диагностику

После `POST /diagnostics` backend публикует событие в `RMQ_DIAGNOSTIC_REQUEST_QUEUE`.

После `PATCH /diagnostics/{id}` с `result_file_id` backend публикует событие в `RMQ_DIAGNOSTIC_RESPONSE_QUEUE`.

## Ограничения и особенности

- максимальный размер загружаемого файла — `1000 МБ`
- файлы сохраняются в S3 / MinIO
- backend не стартует без доступных PostgreSQL, RabbitMQ и S3 / MinIO

## Проверка работоспособности

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:

```json
{"status":"ok"}
```

Логи в Docker:

```bash
docker compose logs -f freeman-backend
```
