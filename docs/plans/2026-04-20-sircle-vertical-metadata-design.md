## Goal

Force all `sircle*.mp4` sends to include vertical video metadata so Telegram receives `width=1080` and `height=1920` for every built-in video asset.

## Scope

- Update all current `answer_video` and `send_video` call sites that send:
  - `sircle1.mp4`
  - `sircle2.mp4`
  - `sircle3.mp4`
  - `sircle4.mp4`
  - `sircle5.mp4`
  - `sircle6.mp4`
- Keep the rest of the message flow unchanged.

## Chosen Approach

Set the metadata directly at each call site:

- `width=1080`
- `height=1920`

## Why This Approach

- Matches the requested behavior with minimal code movement.
- Keeps the change explicit at each send point.
- Avoids adding wrappers or abstractions for a small fixed set of assets.

## Risks

- These values are sender metadata, not a file transformation step.
- Telegram can still use the actual file stream characteristics when rendering the media.

## Verification

- Search for `answer_video(` and `send_video(` in the bot code.
- Confirm every `sircle*.mp4` send includes `width=1080` and `height=1920`.
