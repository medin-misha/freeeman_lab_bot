# Bot

Пользовательский Telegram-бот на `aiogram`, который:

- регистрирует пользователя в `backend`
- отправляет файлы диагностики в `backend`
- получает готовые результаты из RabbitMQ
- присылает пользователю файл результата и открывает следующий шаг сценария

## Запуск

### Локально

```bash
cd bot
uv sync --frozen
uv run python main.py
```

### В Docker Compose

Из корня репозитория:

```bash
docker compose up --build -d freeman-bot
```

Если нужен весь стек:

```bash
docker compose up --build -d
```

## Переменные окружения

Бот читает переменные из `bot/.env`.

Точные имена:

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `TOKEN` | да | токен Telegram-бота |
| `API_URL` | да | URL backend |
| `CHANNEL_ID` | да | канал для проверки подписки |
| `RMQ_URL` | да | RabbitMQ URL |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь с готовыми результатами диагностик |
| `TELEGRAM_BOT_API_URL` | да | адрес локального Telegram Bot API server |

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

- в `docker-compose.yml` `API_URL` дополнительно переопределяется в environment
- `TELEGRAM_BOT_API_URL` должен совпадать с реальным режимом запуска: `localhost` для локального Python-процесса, `telegram-bot-api` для Docker Compose

## Сценарий использования

Основной пользовательский flow:

1. `/start`
2. подписка на канал
3. сообщение `МАСШТАБ`
4. сообщение `ДИАГНОСТИКА`
5. отправка одного файла диагностики
6. при необходимости — отдельное текстовое описание
7. получение результата

Поддерживаемые типы файла диагностики:

- `voice`
- `audio`
- `document`

Лимит:

- максимум `1000 МБ`

Если файл не подходит:

- бот отвечает понятным сообщением, что именно не так
- серверные ошибки не пробрасываются сырыми текстами, пользователь получает сообщение с просьбой обратиться в поддержку

## Что делает бот внутри

- `bot/handlers/system/` — `/start` и системные callbacks
- `bot/handlers/events/scale/` — сценарий `МАСШТАБ`
- `bot/handlers/events/analysis/` — сценарий `РАЗБОР`
- `bot/handlers/events/diagnostics/` — загрузка диагностики и получение результата
- `bot/handlers/errors/` — глобальная маршрутизация ошибок
- `bot/core/utils/api.py` — HTTP-клиент к backend с нормализацией ошибок

## Проверка работоспособности

Проверьте:

- backend доступен по `API_URL`
- RabbitMQ доступен по `RMQ_URL`
- Telegram Bot API доступен по `TELEGRAM_BOT_API_URL`
- бот запущен и polling стартовал без exception в логах

Логи в Docker:

```bash
docker compose logs -f freeman-bot
```
