# Bot

Пользовательский Telegram-бот на `aiogram`, который ведёт пользователя по основным сценариям проекта:

- вход через подписку на канал
- выдача методички
- отправка расширенной диагностики
- переход к разбору
- переход в mini app `Ядро`
- отправка заявок на консультации, регрессии и наставничество

## Запуск

### Локально

```bash
cd bot
uv sync --frozen
uv run python main.py
```

### В Docker Compose

```bash
docker compose up --build -d freeman-bot
```

Для полного стека:

```bash
docker compose up --build -d
```

## Переменные окружения

Бот читает переменные из `bot/.env`.

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `TOKEN` | да | токен Telegram-бота |
| `API_URL` | да | URL backend |
| `TELEGRAM_BOT_API_URL` | да | URL Telegram Bot API |
| `CHANNEL_ID` | да | канал для проверки подписки |
| `RMQ_URL` | да | URL RabbitMQ |
| `RMQ_DIAGNOSTIC_RESPONSE_QUEUE` | да | очередь с готовыми результатами диагностик |
| `RMQ_ANALYSIS_SCHEDULE_CONFIRMATION_QUEUE` | нет | очередь подтверждений записи на разбор |
| `RMQ_CONSULTATION_REQUEST_QUEUE` | нет | очередь заявок на консультации |
| `RMQ_REGRESSION_REQUEST_QUEUE` | нет | очередь заявок на регрессии |
| `RMQ_MENTORSHIP_REQUEST_QUEUE` | нет | очередь заявок на наставничество |
| `CORE_MIN_APP` | да | URL mini app для раздела `Ядро` |

Пример для тестового Compose:

```env
TOKEN=0000000000:TEST_USER_BOT_TOKEN_FOR_LOCAL_TESTS_ONLY
API_URL=http://freeman-backend:8000
CHANNEL_ID=@test_channel
RMQ_URL=amqp://guest:guest@rabbitmq:5672/
RMQ_DIAGNOSTIC_RESPONSE_QUEUE=diagnostic_response
RMQ_ANALYSIS_SCHEDULE_CONFIRMATION_QUEUE=analysis_schedule_confirmation
RMQ_CONSULTATION_REQUEST_QUEUE=consultation_request
RMQ_REGRESSION_REQUEST_QUEUE=regression_request
RMQ_MENTORSHIP_REQUEST_QUEUE=mentorship_request
TELEGRAM_BOT_API_URL=https://api.telegram.org
CORE_MIN_APP=https://example.com
```

## Что делает бот

### Входной сценарий

1. Пользователь отправляет `/start`.
2. Бот показывает кнопку подписки на сообщество и кнопку проверки подписки.
3. После подтверждения подписки бот отправляет preview image, видео и главное меню.

### Главное меню

Доступные разделы:

- `Забрать методичку`
- `Пройти диагностику`
- `Ядро`
- `Еще возможности`

### Методичка

При выборе `Забрать методичку` бот отправляет:

- PDF
- EPUB
- вертикальное видео

### Диагностика

Поддерживается расширенная диагностика:

1. Бот показывает intro-видео и PDF-инструкцию.
2. Пользователь отправляет один файл `voice`, `audio` или `document`.
3. Максимальный размер файла — `1000 МБ`.
4. Если описание не приложено в `caption`, бот запрашивает его отдельным текстовым сообщением.
5. Бот загружает файл в `backend` и создаёт запись диагностики.
6. После получения результата из RabbitMQ бот отправляет:
   - документ с результатом
   - видео результата
   - меню следующего шага

### Разбор

После диагностики пользователь может перейти в сценарий `Пойти в разбор`:

- выбрать формат `public` или `private`
- перейти к расписанию
- подтвердить запись

После подтверждения бот публикует событие в `RMQ_ANALYSIS_SCHEDULE_CONFIRMATION_QUEUE`.

### Ядро

Кнопка `Ядро` открывает Telegram WebApp по адресу из `CORE_MIN_APP`.

### Еще возможности

Раздел содержит:

- консультации
- регрессии
- наставничество
- соцсети
- магазин
- о проекте

Для консультаций, регрессий и наставничества бот публикует сообщения в соответствующие очереди RabbitMQ.

## Внутреннее устройство

- `bot/handlers/system/` — `/start`, проверка подписки, возврат в меню
- `bot/handlers/events/scale/` — выдача методички
- `bot/handlers/events/diagnostics/` — сценарий диагностики и получение результата
- `bot/handlers/events/analysis/` — сценарий разбора
- `bot/handlers/events/nucleus/` — вход в mini app `Ядро`
- `bot/handlers/events/more/` — консультации, регрессии, наставничество и доп. разделы
- `bot/handlers/errors/` — обработка ошибок
- `bot/core/utils/api.py` — HTTP-клиент к backend

## Проверка работоспособности

Проверьте:

- backend доступен по `API_URL`
- RabbitMQ доступен по `RMQ_URL`
- Telegram Bot API доступен по `TELEGRAM_BOT_API_URL`
- polling стартовал без exception в логах

Логи:

```bash
docker compose logs -f freeman-bot
```
