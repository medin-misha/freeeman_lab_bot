## Goal

Notify the admin bot when a user confirms they added themselves to the analysis schedule by clicking `Я внес(ла) себя в расписание`.

## Scope

- Publish a RabbitMQ event from the user bot on schedule confirmation.
- Consume that event in `admin-bot` and fan out a text notification to all configured admin chats.
- Add queue settings and documentation for the new event.

## Chosen Approach

- Add a dedicated queue for analysis schedule confirmations.
- Publish an event with the selected analysis format and the button-click timestamp.
- Keep the user-facing flow unchanged even if admin notification delivery fails.

## Notification Format

`Новая запись на разбор`

`Формат разбора: публичный / приватный`
`● анкета заполнена`
`● расписание подтверждено`
`● дата / время: YYYY-MM-DD HH:MM:SS UTC`

## Why This Approach

- Reuses the existing `bot -> RabbitMQ -> admin-bot` architecture already used for `Ядро`.
- Keeps admin chat IDs isolated inside `admin-bot`.
- Makes the event explicit and easy to evolve later.

## Risks

- Minimal. The new flow is additive.
- If RabbitMQ publishing fails, admins will miss the notification, but the user should still see a successful confirmation.

## Verification

- Click `Я внес(ла) себя в расписание` in both public and private flows.
- Confirm the user still sees the existing success message.
- Confirm `admin-bot` sends the new notification to every configured admin chat.
