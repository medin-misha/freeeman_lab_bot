# freeeman_lab_bot

Монорепозиторий проекта с пользовательским Telegram-ботом, админ-ботом, FastAPI backend, Telegram mini app и локальным Docker-окружением для разработки и тестов.

## Состав репозитория

### Приложение

- `bot` — пользовательский Telegram-бот на `aiogram`
- `admin-bot` — Telegram-бот для администраторов
- `backend` — FastAPI API, PostgreSQL CRUD, работа с файлами и RabbitMQ
- `core-mini-app` — Vue 3 mini app для заявок в `Ядро`

### Инфраструктура в `docker-compose.yml`

- `postgres` — PostgreSQL
- `rabbitmq` — RabbitMQ broker
- `telegram-bot-api` — опциональный локальный Telegram Bot API server
- `freeman-minio` — S3-совместимое файловое хранилище
- `freeman-minio-init` — создание bucket в MinIO
- `nginx` — reverse proxy для mini app, backend API и Grafana

### Мониторинг

- `loki` — хранение логов
- `promtail` — сбор логов контейнеров Docker
- `prometheus` — хранение метрик
- `cadvisor` — метрики контейнеров
- `grafana` — дашборды на основе Loki и Prometheus

## Основные сценарии

### Диагностика

1. Пользователь проходит сценарий в `bot`.
2. `bot` регистрирует пользователя в `backend`, загружает файл диагностики и создаёт запись `/diagnostics`.
3. `backend` сохраняет файл в S3 / MinIO и публикует событие в `RMQ_DIAGNOSTIC_REQUEST_QUEUE`.
4. `admin-bot` получает сообщение из очереди, рассылает уведомление администраторам и ждёт файл результата.
5. Администратор загружает результат через `admin-bot`.
6. `admin-bot` отправляет файл в `backend`, а затем обновляет диагностику через `PATCH /diagnostics/{id}`.
7. `backend` публикует событие о готовом результате в `RMQ_DIAGNOSTIC_RESPONSE_QUEUE`.
8. `bot` получает событие, отправляет пользователю результат и открывает следующий шаг сценария.

### Разбор и дополнительные заявки

- `bot` публикует подтверждение записи на разбор в `RMQ_ANALYSIS_SCHEDULE_CONFIRMATION_QUEUE`
- `bot` публикует запросы на консультацию, регрессию и наставничество в отдельные очереди
- `admin-bot` слушает эти очереди и рассылает уведомления в `CHAT_IDS`

### Mini app `Ядро`

1. Пользователь нажимает кнопку `Узнать про ядро` в `bot`.
2. Открывается `core-mini-app`.
3. Mini app отправляет форму в `POST /core/submit`.
4. `backend` обновляет профиль пользователя, создаёт заявку `Core` и публикует событие в `RMQ_NUCLEUS_APPLICATION_QUEUE`.
5. `admin-bot` получает уведомление о новой заявке.

## Что нужно для запуска

- Docker и Docker Compose plugin
- Python `3.11+` и `uv`, если хотите запускать Python-сервисы локально
- Node.js `20.19+` или `22.12+`, если хотите запускать `core-mini-app` без Docker

Важно:

- основной `docker-compose.yml` — это локальный / тестовый стек
- production-секреты и production-токены не должны попадать в локальные `.env`
- локальный `telegram-bot-api` включается только через profile `local-telegram-api`

## Быстрый запуск через Docker Compose

### 1. Подготовьте `.env` файлы

Нужны файлы:

- `.env`
- `backend/.env`
- `bot/.env`
- `admin-bot/.env`
- `core-mini-app/.env`

Шаблоны:

- `.env.example`
- `backend/.env.example`
- `bot/.env.example`
- `admin-bot/.env.example`
- `core-mini-app/.env.example`

### 2. Запустите стек

```bash
docker compose up --build -d
```

Проверка статуса:

```bash
docker compose ps
```

Основные логи:

```bash
docker compose logs -f freeman-backend
docker compose logs -f freeman-bot
docker compose logs -f freeman-admin-bot
docker compose logs -f freeman-mini-app
docker compose logs -f nginx
```

Остановка:

```bash
docker compose down
```

### 3. Примените миграции

Если база пустая:

```bash
cd backend
uv run alembic upgrade head
```

### 4. Проверьте HTTP endpoints

- backend health: `http://localhost:8000/health`
- mini app через nginx: `http://localhost/app/`
- backend API через nginx: `http://localhost/api/`
- Grafana через nginx: `http://localhost/grafana/`

## Локальный запуск без Docker

Если хотите запускать процессы напрямую, отдельно поднимите инфраструктуру:

```bash
docker compose up -d postgres rabbitmq freeman-minio freeman-minio-init
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

### Mini app

```bash
cd core-mini-app
pnpm install
pnpm dev
```

## Переменные окружения

### Корневой `.env`

Используется в основном для compose-стека:

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `COMPOSE_PROJECT_NAME` | нет | префикс проекта Docker Compose |
| `TELEGRAM_API_ID` | нет | app id для локального `telegram-bot-api` |
| `TELEGRAM_API_HASH` | нет | app hash для локального `telegram-bot-api` |
| `GRAFANA_ADMIN_PASSWORD` | нет | пароль администратора Grafana |
| `MINIO_ROOT_USER` | нет | root user для MinIO |
| `MINIO_ROOT_PASSWORD` | нет | root password для MinIO |

### `backend/.env`

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `DATABASE` | да | SQLAlchemy DSN для PostgreSQL |
| `AWS_S3_ACCESS_KEY` | да | access key для S3 / MinIO |
| `AWS_S3_SECRERT_KEY` | да | secret key для S3 / MinIO |
| `AWS_S3_BUCKET_NAME` | да | bucket для хранения файлов |
| `AWS_S3_ENDPOINT_URL` | да | endpoint S3 / MinIO |
| `RMQ_URL` | да | URL RabbitMQ |
| `RMQ_DIAGNOSTIC_REQUEST_QUEUE` | да | очередь новых диагностик |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь готовых результатов |
| `RMQ_NUCLEUS_APPLICATION_QUEUE` | нет | очередь заявок в `Ядро` |

Важно:

- код ожидает переменную именно `AWS_S3_SECRERT_KEY`
- опечатку в имени нужно повторять один в один

### `bot/.env`

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `TOKEN` | да | токен пользовательского Telegram-бота |
| `API_URL` | да | URL backend |
| `TELEGRAM_BOT_API_URL` | да | URL Telegram Bot API |
| `CHANNEL_ID` | да | канал или chat id для проверки подписки |
| `RMQ_URL` | да | URL RabbitMQ |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь готовых результатов диагностик |
| `RMQ_ANALYSIS_SCHEDULE_CONFIRMATION_QUEUE` | нет | очередь подтверждений записи на разбор |
| `RMQ_CONSULTATION_REQUEST_QUEUE` | нет | очередь заявок на консультации |
| `RMQ_REGRESSION_REQUEST_QUEUE` | нет | очередь заявок на регрессии |
| `RMQ_MENTORSHIP_REQUEST_QUEUE` | нет | очередь заявок на наставничество |
| `CORE_MIN_APP` | да | URL mini app для кнопки `Ядро` |

### `admin-bot/.env`

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `TOKEN` | да | токен admin-бота |
| `API_URL` | да | URL backend |
| `API_TIMEOUT_SECONDS` | нет | timeout запросов к backend |
| `TELEGRAM_BOT_API_URL` | да | URL Telegram Bot API |
| `RMQ_URL` | да | URL RabbitMQ |
| `RMQ_DIAGNOSTIC_REQUEST_QUEUE` | да | очередь новых диагностик |
| `RMQ_NUCLEUS_APPLICATION_QUEUE` | нет | очередь заявок в `Ядро` |
| `RMQ_ANALYSIS_SCHEDULE_CONFIRMATION_QUEUE` | нет | очередь подтверждений записи на разбор |
| `RMQ_CONSULTATION_REQUEST_QUEUE` | нет | очередь заявок на консультации |
| `RMQ_REGRESSION_REQUEST_QUEUE` | нет | очередь заявок на регрессии |
| `RMQ_MENTORSHIP_REQUEST_QUEUE` | нет | очередь заявок на наставничество |
| `CHAT_IDS` | да | список chat id администраторов через запятую |

### `core-mini-app/.env`

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `VITE_API_URL` | да | базовый URL backend API для mini app |

Для docker / nginx по умолчанию используется:

```env
VITE_API_URL=/api
```

## Мониторинг

### Доступные интерфейсы

| Сервис | Адрес |
| --- | --- |
| Grafana | `http://localhost/grafana/` |
| Prometheus | `http://localhost:9090` |
| Loki | `http://localhost:3100` |

### Что реально провиженится из репозитория

- datasource `Prometheus`
- datasource `Loki`
- dashboard provider из `monitoring/grafana/dashboards`

Сейчас в репозитории нет файлов provisioning для contact points, notification policies и alert rules, поэтому готовые Telegram-алерты автоматически не поднимаются.

### Логи мониторинга

```bash
docker compose logs -f nginx
docker compose logs -f grafana
docker compose logs -f loki
docker compose logs -f promtail
docker compose logs -f prometheus
```

## Частые проблемы

### Backend не стартует

Проверьте:

- доступность PostgreSQL по `DATABASE`
- применены ли миграции
- доступность RabbitMQ по `RMQ_URL`
- корректность `AWS_S3_*`

### Бот не может обратиться к backend или RabbitMQ

Проверьте:

- `API_URL`
- `RMQ_URL`
- `TELEGRAM_BOT_API_URL`
- наличие нужных очередей в `.env`

### Mini app открывается, но не отправляет форму

Проверьте:

- `CORE_MIN_APP` в `bot/.env`
- `VITE_API_URL` в `core-mini-app/.env`
- доступность `POST /core/submit`
- наличие пользователя в backend с `chat_id`, совпадающим с Telegram user id

## Где смотреть подробнее

- [bot/README.md](./bot/README.md)
- [admin-bot/README.md](./admin-bot/README.md)
- [backend/README.md](./backend/README.md)
- [core-mini-app/README.md](./core-mini-app/README.md)
