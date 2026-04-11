# Admin Bot Diagnostic Description

## Goal

Show the diagnostic `description` in `admin-bot` when a new diagnostic request is received through AMQP.

## Scope

- Ensure the backend publishes a serialized diagnostic request payload that includes `description`.
- Parse `description` in `admin-bot` from the incoming AMQP message.
- Render the description in the admin notification text before sending the source file.

## Design

- Backend publisher normalizes pydantic payloads to plain dictionaries with `model_dump(mode="json")`.
- Admin bot extracts `description` from the message payload and interpolates it into the notification text.
- If `description` is empty or missing, the notification falls back to a readable default.

## Risks

- Old messages without `description` remain valid because the field is optional.
- The notification template must stay compatible with `.format(...)` arguments.
