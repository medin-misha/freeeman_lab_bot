# Vertical Videos Design

## Goal

Convert all videos in `bot/files/videos/` from horizontal `1920x1080` to vertical `1080x1920` without black bars.

## Chosen Approach

Add a small batch-processing script that uses `ffmpeg` to scale each source video to height `1920` and then hard-crop the width to `1080`.

## Why This Approach

- Keeps the result reproducible instead of relying on one-off terminal commands.
- Supports per-file crop offsets when center-crop is not visually acceptable.
- Preserves existing bot integration because output files can replace the current `.mov` files in place.

## Processing Flow

- Iterate over all `*.mov` files in `bot/files/videos/`.
- Scale each video to `height=1920` with aspect ratio preserved.
- Crop to `1080x1920`.
- Allow an optional per-file horizontal offset to shift the crop window.
- Write to a temporary file first and only replace the source after successful encoding.

## Verification

- Use `ffprobe` to confirm every output file is `1080x1920`.
- Extract sample frames for visual inspection.
- If a video is framed poorly, adjust the configured offset and rerun the script.

## Notes

- Bot code does not need to change because file names stay the same.
- Existing unrelated workspace changes should remain untouched.
