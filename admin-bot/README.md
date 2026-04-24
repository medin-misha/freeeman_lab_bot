# Admin Bot

Админский Telegram-бот на `aiogram`, который получает события из RabbitMQ и рассылает уведомления администраторам из списка `CHAT_IDS`.

## Что умеет

- уведомлять о новых диагностиках
- принимать файл результата диагностики и сохранять его через `backend`
- уведомлять о новой заявке в `Ядро`
- уведомлять о подтверждении записи на разбор
- уведомлять о запросах на консультации, регрессии и наставничество

## Запуск

### Локально

```bash
cd admin-bot
uv sync --frozen
uv run python main.py
```

### В Docker Compose

```bash
docker compose up --build -d freeman-admin-bot
```

## Переменные окружения

Бот читает переменные из `admin-bot/.env`.

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
| `CHAT_IDS` | да | список Telegram chat id администраторов через запятую |

`CHAT_IDS` должен содержать numeric id чатов, например:

```env
CHAT_IDS=123456789,-100987654321
```

## Поведение

### Диагностика

1. `backend` публикует сообщение в `RMQ_DIAGNOSTIC_REQUEST_QUEUE`.
2. `admin-bot` получает `diagnostic_id`, `file_id`, `user_id` и описание.
3. Бот отправляет администраторам:
   - текст уведомления
   - исходный файл пользователя
   - inline-кнопку `Отправить результат`
4. После нажатия кнопки бот переводит чат в режим ожидания файла результата.
5. Администратор отправляет `document` или `audio`.
6. Бот загружает файл в `backend`, обновляет диагностику и очищает inline-кнопку у исходного уведомления.

Само сообщение пользователю о готовом результате отправляет не `admin-bot`, а пользовательский `bot` после события из `RMQ_DIAGNOSTIC_RESPONSE_QUEUE`.

### Остальные очереди

Отдельные обработчики слушают:

- `RMQ_NUCLEUS_APPLICATION_QUEUE`
- `RMQ_ANALYSIS_SCHEDULE_CONFIRMATION_QUEUE`
- `RMQ_CONSULTATION_REQUEST_QUEUE`
- `RMQ_REGRESSION_REQUEST_QUEUE`
- `RMQ_MENTORSHIP_REQUEST_QUEUE`

Для этих событий бот отправляет администраторам текстовые уведомления.

## Ограничения

- сообщения и callbacks из чатов вне `CHAT_IDS` игнорируются
- `/start` отвечает только в разрешённых чатах
- для загрузки результата диагностики принимаются только `document` и `audio`

## Внутреннее устройство

- `admin-bot/core/rmq.py` — RabbitMQ broker
- `admin-bot/core/utils/api.py` — HTTP-клиент к backend
- `admin-bot/handlers/events/diagnostics/` — обработка новых диагностик и загрузка результата
- `admin-bot/handlers/events/nucleus/` — заявки mini app `Ядро`
- `admin-bot/handlers/events/analysis/` — подтверждения записи на разбор
- `admin-bot/handlers/events/consultations/` — заявки на консультации
- `admin-bot/handlers/events/regressions/` — заявки на регрессии
- `admin-bot/handlers/events/mentorship/` — заявки на наставничество

## Проверка работоспособности

Проверьте:

- backend доступен по `API_URL`
- RabbitMQ доступен по `RMQ_URL`
- `CHAT_IDS` заполнен корректно
- бот запущен и получает сообщения из очередей

Логи:

```bash
docker compose logs -f freeman-admin-bot
```
