# Admin Bot

Separate Telegram admin bot that listens to RabbitMQ and sends notifications to a fixed list of chat IDs.

## Environment

Create `admin-bot/.env` with:

- `TOKEN`
- `RMQ_URL`
- `RMQ_DIAGNOSTIC_REQUEST_QUEUE`
- `CHAT_IDS`

`CHAT_IDS` must be a comma-separated list of Telegram chat IDs.

## Behavior

- queue message -> sends `Новая заявка диагностики` to all configured chats
- `/start` from an allowed chat -> replies `Admin bot active`
- any other chat is ignored
