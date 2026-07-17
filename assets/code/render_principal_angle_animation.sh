#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
media_dir="${TMPDIR:-/tmp}/principal-angle-manim"
scene_file="$repo_root/assets/code/principal_angle_animation.py"
source_video="$media_dir/videos/principal_angle_animation/720p30/principal-angle-mechanism-source.mp4"
output_dir="$repo_root/assets/video"

mkdir -p "$output_dir"

manim -qm \
  --media_dir "$media_dir" \
  "$scene_file" \
  PrincipalAngleMechanism \
  -o principal-angle-mechanism-source.mp4

# Preserve the deliberate scene timing. The animation is paced as a guided
# explanation rather than compressed to a fixed short duration.
ffmpeg -y -hide_banner -loglevel error \
  -i "$source_video" \
  -an \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
  -movflags +faststart \
  "$output_dir/principal-angle-mechanism.mp4"

ffmpeg -y -hide_banner -loglevel error \
  -i "$source_video" \
  -an \
  -c:v libvpx-vp9 -crf 34 -b:v 0 -row-mt 1 \
  "$output_dir/principal-angle-mechanism.webm"

ffmpeg -y -hide_banner -loglevel error \
  -ss 31 \
  -i "$output_dir/principal-angle-mechanism.mp4" \
  -frames:v 1 -q:v 3 \
  "$repo_root/assets/images/principal-angle-mechanism-poster.jpg"

ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 \
  "$output_dir/principal-angle-mechanism.mp4"
