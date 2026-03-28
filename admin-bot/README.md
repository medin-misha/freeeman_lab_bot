# Admin Bot

Separate Telegram admin bot built on `aiogram` that listens to RabbitMQ and sends diagnostic requests to a fixed list of chat IDs.

## Environment

Create `admin-bot/.env` with:

- `TOKEN`
- `API_URL`
- `RMQ_URL`
- `RMQ_DIAGNOSTIC_REQUEST_QUEUE`
- `CHAT_IDS`

`CHAT_IDS` must be a comma-separated list of Telegram chat IDs.

## Behavior

- queue message with `id`, `file_id`, `user_id` -> sends a notification, source voice, and "Отправить результат" button to all configured chats
- `/start` from an allowed chat -> replies `Admin bot active`
- clicking the result button -> puts the chat into result upload mode
- sending a document or audio file in that mode -> uploads the file to backend and marks the diagnostic as completed
- any message or callback from an unlisted chat is ignored
