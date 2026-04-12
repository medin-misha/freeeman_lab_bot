# freeeman_lab_bot

Монорепозиторий с тремя сервисами:

- `backend` — FastAPI API для пользователей, файлов и диагностик
- `bot` — пользовательский Telegram-бот на `aiogram`
- `admin-bot` — Telegram-бот для администраторов, который получает задачи из RabbitMQ и загружает результаты диагностик

В репозитории также есть инфраструктурные сервисы для локальной разработки:

- `telegram-bot-api` — локальный Telegram Bot API server
- `freeman-minio` — S3-совместимое хранилище файлов
- `freeman-minio-init` — инициализация bucket в MinIO

## Как это работает

Основной сценарий такой:

1. Пользователь взаимодействует с `bot`.
2. `bot` отправляет файл и метаданные в `backend`.
3. `backend` сохраняет файл в S3 и публикует запрос на диагностику в RabbitMQ.
4. `admin-bot` получает запрос из очереди и уведомляет администратора.
5. Администратор загружает результат через `admin-bot`.
6. `backend` публикует событие с готовым результатом в очередь ответа.
7. `bot` получает событие и отправляет пользователю готовый файл.

## Что нужно для запуска

Обязательные зависимости:

- Docker и Docker Compose plugin
- Python `3.11+` и `uv`, если хотите запускать сервисы локально без Docker
- доступный PostgreSQL
- доступный RabbitMQ

Важно:

- текущий `docker-compose.yml` **не поднимает PostgreSQL и RabbitMQ**
- перед запуском нужно либо использовать уже существующие инстансы, либо добавить свои сервисы самостоятельно
- `MinIO` и `telegram-bot-api` compose поднимает сам

## Быстрый запуск через Docker Compose

### 1. Подготовьте `.env` файлы

Создайте или обновите:

- `backend/.env`
- `bot/.env`
- `admin-bot/.env`

Готовые шаблоны:

- `backend/.env.example`
- `bot/.env.example`
- `admin-bot/.env.example`

### 2. Убедитесь, что PostgreSQL и RabbitMQ доступны контейнерам

Переменные `DATABASE` и `RMQ_URL` должны указывать на адреса, достижимые **изнутри контейнеров**.

Примеры:

- внешний сервер: `postgresql+asyncpg://user:pass@10.0.0.5:5432/app`
- macOS/Windows host service: `postgresql+asyncpg://user:pass@host.docker.internal:5432/app`
- Linux host service: либо реальный IP хоста, либо отдельный сервис в `docker-compose.yml`

То же относится к `RMQ_URL`.

### 3. Запустите сервисы

Из корня репозитория:

```bash
docker compose up --build -d
```

Проверка статуса:

```bash
docker compose ps
```

Логи:

```bash
docker compose logs -f freeman-backend
docker compose logs -f freeman-bot
docker compose logs -f freeman-admin-bot
docker compose logs -f telegram-bot-api
docker compose logs -f freeman-minio
```

Остановка:

```bash
docker compose down
```

### 4. Проверьте backend

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:

```json
{"status":"ok"}
```

### 5. Примените миграции

Если база пустая, примените миграции отдельно:

```bash
cd backend
uv run alembic upgrade head
```

Если backend уже запущен в контейнере, ту же команду можно выполнить локально из директории `backend`, используя тот же `.env`.

## Локальный запуск без Docker

Этот режим нужен, если вы хотите запускать Python-процессы напрямую, а инфраструктуру поднять отдельно.

### Инфраструктура

Нужно поднять:

- PostgreSQL
- RabbitMQ
- MinIO
- Telegram Bot API server

Из compose можно использовать только инфраструктурные сервисы, если PostgreSQL и RabbitMQ у вас внешние:

```bash
docker compose up -d telegram-bot-api freeman-minio freeman-minio-init
```

### Backend

```bash
cd backend
uv sync --frozen
uv run alembic upgrade head
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Пользовательский бот

```bash
cd bot
uv sync --frozen
uv run python main.py
```

### Админ-бот

```bash
cd admin-bot
uv sync --frozen
uv run python main.py
```

## Переменные окружения

### `backend/.env`

Используются exact-имена переменных:

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `DATABASE` | да | SQLAlchemy DSN для PostgreSQL. Формат: `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB_NAME` |
| `AWS_S3_ACCESS_KEY` | да | access key для S3 / MinIO |
| `AWS_S3_SECRERT_KEY` | да | secret key для S3 / MinIO |
| `AWS_S3_BUCKET_NAME` | да | bucket для загрузки файлов |
| `AWS_S3_ENDPOINT_URL` | да | endpoint S3 / MinIO |
| `RMQ_URL` | да | URL подключения к RabbitMQ |
| `RMQ_DIAGNOSTIC_REQUEST_QUEUE` | да | очередь, в которую backend публикует новые диагностики |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь, в которую backend публикует готовые результаты |

Важно:

- переменная называется именно `AWS_S3_SECRERT_KEY`
- в названии есть опечатка `SECRERT`, и документация должна повторять её ровно так, как ожидает код

Пример для локальной разработки:

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

Пример для Docker Compose:

```env
DATABASE=postgresql+asyncpg://postgres:postgres@host.docker.internal:5432/freeman
AWS_S3_ACCESS_KEY=admin
AWS_S3_SECRERT_KEY=supersecretpassword
AWS_S3_BUCKET_NAME=freeman-bucket
AWS_S3_ENDPOINT_URL=http://freeman-minio:9000
RMQ_URL=amqp://guest:guest@host.docker.internal:5672/
RMQ_DIAGNOSTIC_REQUEST_QUEUE=diagnostic_request
RMQ_DIAGNOSTIC_RESPONSE_QUEUE=diagnostic_response
```

### `bot/.env`

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `TOKEN` | да | токен пользовательского Telegram-бота |
| `API_URL` | да | базовый URL backend |
| `CHANNEL_ID` | да | Telegram channel username или chat id для проверки подписки |
| `RMQ_URL` | да | URL RabbitMQ для очереди ответов |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь, из которой бот получает готовые диагностики |
| `TELEGRAM_BOT_API_URL` | да | URL локального Telegram Bot API server |

Пример для локального запуска:

```env
TOKEN=123456:telegram-token
API_URL=http://localhost:8000
CHANNEL_ID=@your_channel
RMQ_URL=amqp://guest:guest@localhost:5672/
RMQ_DIAGNOSTIC_RESPONSE_QUEUE=diagnostic_response
TELEGRAM_BOT_API_URL=http://localhost:8081
```

Пример для Docker Compose:

```env
TOKEN=123456:telegram-token
API_URL=http://freeman-backend:8000
CHANNEL_ID=@your_channel
RMQ_URL=amqp://guest:guest@host.docker.internal:5672/
RMQ_DIAGNOSTIC_RESPONSE_QUEUE=diagnostic_response
TELEGRAM_BOT_API_URL=http://telegram-bot-api:8081
```

Важно:

- в `docker-compose.yml` `API_URL` для `freeman-bot` переопределяется на `http://freeman-backend:8000`
- `TELEGRAM_BOT_API_URL` не переопределяется, его нужно выставить корректно в `.env`

### `admin-bot/.env`

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `TOKEN` | да | токен admin Telegram-бота |
| `API_URL` | да | базовый URL backend |
| `API_TIMEOUT_SECONDS` | да | timeout запросов к backend в секундах |
| `TELEGRAM_BOT_API_URL` | да | URL локального Telegram Bot API server |
| `RMQ_URL` | да | URL RabbitMQ |
| `RMQ_DIAGNOSTIC_REQUEST_QUEUE` | да | очередь входящих диагностик |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь исходящих результатов |
| `CHAT_IDS` | да | список Telegram chat id администраторов через запятую |

Пример:

```env
TOKEN=123456:telegram-token
API_URL=http://localhost:8000
API_TIMEOUT_SECONDS=600
TELEGRAM_BOT_API_URL=http://localhost:8081
RMQ_URL=amqp://guest:guest@localhost:5672/
RMQ_DIAGNOSTIC_REQUEST_QUEUE=diagnostic_request
RMQ_DIAGNOSTIC_RESPONSE_QUEUE=diagnostic_response
CHAT_IDS=123456789,-1001234567890
```

## Как пользоваться сервисами

### Пользовательский бот

Основной flow:

1. Пользователь отправляет `/start`.
2. Бот предлагает подписаться на канал.
3. После подписки пользователь пишет `МАСШТАБ`.
4. Бот отправляет материалы и предлагает пройти диагностику.
5. Пользователь пишет `ДИАГНОСТИКА`.
6. Бот отправляет инструкцию и ждёт один файл: `voice`, `audio` или `document`.
7. Максимальный размер файла — `1000 МБ`.
8. Если описания нет в caption, бот просит прислать его отдельным текстовым сообщением.
9. Когда результат готов, бот отправляет файл и открывает доступ к разбору.

Что считается корректным файлом диагностики:

- `voice`
- `audio`
- `document`

Что не пройдёт:

- фото, видео, стикеры, любые другие типы вложений
- файл больше `1000 МБ`

### Admin bot

Основной flow:

1. `backend` кладёт новую диагностику в `RMQ_DIAGNOSTIC_REQUEST_QUEUE`.
2. `admin-bot` отправляет уведомление администраторам из `CHAT_IDS`.
3. Администратор нажимает кнопку отправки результата.
4. `admin-bot` ждёт `document` или `audio` с результатом.
5. Файл загружается в `backend`, диагностика помечается как завершённая.
6. `backend` публикует сообщение в `RMQ_DIAGNOSTIC_RESPONSE_QUEUE`.
7. Пользовательский `bot` отправляет результат пользователю.

## Частые проблемы

### Backend не стартует

Проверьте:

- доступность PostgreSQL по `DATABASE`
- применены ли миграции
- доступность RabbitMQ по `RMQ_URL`
- корректность `AWS_S3_*`

### Бот не может отправить или получить файлы

Проверьте:

- доступность `TELEGRAM_BOT_API_URL`
- поднят ли сервис `telegram-bot-api`
- совпадает ли `API_URL` с реальным адресом backend
- доступен ли MinIO / S3

### Admin bot молчит

Проверьте:

- что сообщения действительно публикуются в `RMQ_DIAGNOSTIC_REQUEST_QUEUE`
- что `CHAT_IDS` заполнен корректными numeric Telegram id
- что админ общался с ботом и бот не заблокирован

## Полезные команды

### Docker

```bash
docker compose ps
docker compose logs -f freeman-backend
docker compose logs -f freeman-bot
docker compose logs -f freeman-admin-bot
docker compose restart freeman-backend
docker compose restart freeman-bot
docker compose restart freeman-admin-bot
```

### Backend

```bash
cd backend
uv sync --frozen
uv run alembic upgrade head
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Bot

```bash
cd bot
uv sync --frozen
uv run python main.py
```

### Admin bot

```bash
cd admin-bot
uv sync --frozen
uv run python main.py
```

## Где смотреть подробнее

- [bot/README.md](./bot/README.md)
- [backend/README.md](./backend/README.md)
- [admin-bot/README.md](./admin-bot/README.md)
