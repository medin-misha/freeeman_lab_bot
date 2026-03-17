# freeeman_lab_bot

Проект состоит из двух сервисов:

- `backend` - FastAPI API
- `bot` - Telegram-бот на `aiogram`

Запуск сделан через Docker Compose из корня репозитория.

## Структура `.env`

### `backend/.env`

Создайте файл `backend/.env` и укажите строку подключения к базе:

```env
DATABASE=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB_NAME
```

Пример:

```env
DATABASE=postgresql+asyncpg://postgres:postgres@db:5432/app
```

### `bot/.env`

Создайте файл `bot/.env` и заполните:

```env
TOKEN=your_telegram_bot_token
API_URL=http://localhost:8000
CHANNEL_ID=@your_channel
```

Где:

- `TOKEN` - токен Telegram-бота от BotFather
- `API_URL` - адрес backend для локального запуска без Docker
- `CHANNEL_ID` - username канала или chat id, который использует бот

## Важно про Docker

При запуске через `docker compose` значение `API_URL` из `bot/.env` автоматически переопределяется на:

```env
API_URL=http://backend:8000
```

Это нужно, чтобы контейнер `bot` обращался к контейнеру `backend` по имени сервиса внутри Docker-сети.

## Запуск через Docker

Из корня проекта выполните:

```bash
docker compose up --build -d
```

Проверить статус контейнеров:

```bash
docker compose ps
```

Посмотреть логи:

```bash
docker compose logs -f
```

Остановить проект:

```bash
docker compose down
```

## Что поднимется

- `backend` будет доступен с хоста на `http://localhost:8000`
- `bot` будет работать в отдельном контейнере
- оба контейнера подключены к общей сети `freeeman-network`

Проверка backend:

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:

```json
{"status":"ok"}
```

## Полезно знать

- `Dockerfile` есть отдельно в `backend/` и `bot/`
- `.env` файлы копируются внутрь контейнеров при сборке образов
- если меняли `.env`, безопаснее пересобрать контейнеры:

```bash
docker compose up --build -d
```
