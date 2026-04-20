## Goal

Force all bot `send_video` calls to include vertical video metadata so Telegram receives `width=1080` and `height=1920` on every send.

## Scope

- Update every current `send_video` call in `bot/` and `admin-bot/`.
- Do not change file paths, captions, reply markup, or any surrounding delivery logic.

## Chosen Approach

Use direct call-site updates and hardcode:

- `width=1080`
- `height=1920`

## Why This Approach

- Matches the requested behavior exactly.
- Keeps the change minimal and easy to audit.
- Avoids adding wrappers or config that are unnecessary for a single known use case.

## Risks

- Telegram may still rely on actual video stream metadata and rendering behavior, so this is a preference hint rather than a hard guarantee for display orientation.
- If a truly horizontal file is sent with vertical metadata, the metadata may not fully override Telegram's media handling.

## Verification

- Search the repository for `send_video(` and confirm each occurrence includes `width=1080` and `height=1920`.
