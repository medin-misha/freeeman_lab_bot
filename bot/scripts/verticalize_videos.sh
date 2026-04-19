#!/usr/bin/env bash

set -euo pipefail

VIDEOS_DIR="${1:-bot/files/videos}"
MODE="${2:---preview}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required" >&2
  exit 1
fi

if ! command -v ffprobe >/dev/null 2>&1; then
  echo "ffprobe is required" >&2
  exit 1
fi

if [[ ! -d "$VIDEOS_DIR" ]]; then
  echo "Videos directory not found: $VIDEOS_DIR" >&2
  exit 1
fi

declare -A OFFSETS=(
  [sircle1.mov]=0
  [sircle2.mov]=0
  [sircle3.mov]=0
  [sircle4.mov]=0
  [sircle5.mov]=0
  [sircle6.mov]=0
)

for input in "$VIDEOS_DIR"/*.mov; do
  [[ -e "$input" ]] || continue

  filename="$(basename "$input")"
  stem="${filename%.mov}"
  offset="${OFFSETS[$filename]:-0}"

  width="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$input")"
  height="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$input")"

  if [[ "$width" -eq 1080 && "$height" -eq 1920 && "$MODE" == "--replace" ]]; then
    echo "skip $filename: already 1080x1920"
    continue
  fi

  output="$VIDEOS_DIR/${stem}_vertical.mov"
  if [[ "$MODE" == "--replace" ]]; then
    output="$VIDEOS_DIR/${stem}.vertical.tmp.mov"
  fi

  scaled_width="$(awk -v w="$width" -v h="$height" 'BEGIN {
    scaled = int((w * 1920 / h) + 0.5)
    if (scaled % 2 != 0) {
      scaled += 1
    }
    print scaled
  }')"
  crop_x="$(( (scaled_width - 1080) / 2 + offset ))"
  if (( crop_x < 0 )); then
    crop_x=0
  fi
  max_crop_x="$(( scaled_width - 1080 ))"
  if (( crop_x > max_crop_x )); then
    crop_x="$max_crop_x"
  fi

  vf="scale=-2:1920:flags=lanczos,crop=1080:1920:${crop_x}:0"

  echo "process $filename with offset=$offset"
  ffmpeg -y \
    -i "$input" \
    -vf "$vf" \
    -c:v libx264 \
    -preset medium \
    -crf 18 \
    -c:a aac \
    -movflags +faststart \
    "$output"

  if [[ "$MODE" == "--replace" ]]; then
    mv "$output" "$input"
  fi
done
