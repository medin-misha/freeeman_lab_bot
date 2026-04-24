# core-mini-app

Telegram mini app на `Vue 3 + Vite`, который открывается из пользовательского бота по кнопке `Ядро` и отправляет заявку в backend.

## Что делает mini app

- показывает многоэкранный onboarding
- собирает форму заявки в `Ядро`
- читает Telegram user id через `@telegram-apps/sdk`
- отправляет форму в `POST /core/submit`

## Запуск

### Локально

```bash
cd core-mini-app
pnpm install
pnpm dev
```

### Production build

```bash
pnpm build
```

### Preview

```bash
pnpm preview
```

### В Docker Compose

Mini app собирается в отдельный контейнер `freeman-mini-app` и публикуется наружу через `nginx`.

Доступ:

- напрямую в compose-сети: `http://freeman-mini-app/`
- через nginx: `http://localhost/app/`

## Переменные окружения

Используется `core-mini-app/.env`.

| Переменная | Обязательна | Описание |
| --- | --- | --- |
| `VITE_API_URL` | да | базовый URL backend API |

Для Docker / nginx по умолчанию:

```env
VITE_API_URL=/api
```

Это позволяет mini app обращаться к backend через nginx route `/api/`.

## Интеграция с Telegram

Mini app использует `@telegram-apps/sdk` для:

- инициализации приложения
- восстановления init data
- чтения текущего пользователя
- haptic feedback
- управления viewport

Если Telegram SDK недоступен, приложение не падает, а пишет предупреждение в console.

## Flow формы

1. Пользователь открывает mini app из бота.
2. Приложение проходит splash screen и onboarding-экраны.
3. Пользователь заполняет форму.
4. На submit приложение берёт `user.id` из Telegram init data.
5. Запрос уходит в `POST ${VITE_API_URL}/core/submit`.
6. После успешного ответа показывается экран успеха.

## Технологии

- Vue 3
- Vite
- `@telegram-apps/sdk`

## Структура

- `src/App.vue` — маршрутизация экранов внутри приложения
- `src/composables/useTelegram.js` — Telegram SDK integration
- `src/composables/useForm.js` — состояние формы, валидация и submit
- `src/components/screens/` — onboarding-экраны
- `src/components/form/` — шаги формы

## Проверка работоспособности

Проверьте:

- `VITE_API_URL` указывает на живой backend
- mini app открывается по `/app/`
- `POST /core/submit` доступен и отвечает без 404/500

Если запускаете вне Telegram, часть интеграции SDK будет работать в деградированном режиме.
