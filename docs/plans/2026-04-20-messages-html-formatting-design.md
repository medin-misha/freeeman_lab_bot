## Goal

Improve the readability of `bot/messages.json` and `admin-bot/messages.json` without changing the meaning of the text.

## Scope

- Reformat message bodies visually with clearer spacing, HTML emphasis, and consistent list markers.
- Keep the same message keys, placeholders, and overall wording.
- Enable HTML parse mode in `admin-bot` so HTML markup in admin messages is rendered.

## Chosen Approach

- Preserve the existing text content and flow.
- Change only the visual presentation:
  - headings via `<b>`
  - secondary hints via `<i>`
  - consistent bullet marker `•`
  - cleaner paragraph breaks

## Why This Approach

- Improves readability without changing business logic or callback wiring.
- Keeps content stable for the current flow while making messages easier to scan in Telegram.
- Avoids risky copy changes.

## Risks

- Very low. The main runtime dependency is HTML parsing in `admin-bot`, which is enabled in this change.

## Verification

- Validate both JSON files.
- Ensure `admin-bot` uses HTML parse mode.
- Spot-check key user and admin messages in Telegram after restart.
