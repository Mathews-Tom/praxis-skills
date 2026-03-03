#!/bin/bash
# render.sh — Render a Remotion composition with quality presets and format options.
#
# Usage:
#   bash render.sh [OPTIONS]
#
# Options:
#   --project DIR         Project directory (default: current directory)
#   --composition ID      Composition ID to render (required)
#   --quality PRESET      preview | draft | final | 4k (default: final)
#   --format FORMAT       mp4 | webm | gif (default: mp4)
#   --output PATH         Output file path (default: out/<composition>.<format>)
#   --props JSON          Props JSON string (optional)
#   --props-file PATH     Path to props JSON file (optional)
#   --concurrency N       Parallel rendering threads (default: auto per quality)
#   --frames RANGE        Frame range, e.g. 0-89 (optional)
#
# Examples:
#   bash render.sh --composition MyVideo
#   bash render.sh --composition ProductDemo --quality draft --format webm
#   bash render.sh --composition UserCard --quality final --props '{"name":"Alice"}'
#   bash render.sh --composition MyVideo --frames 0-89 --quality preview

set -euo pipefail

# ── Defaults ─────────────────────────────────────────────────────────────────

PROJECT_DIR="."
COMPOSITION=""
QUALITY="final"
FORMAT="mp4"
OUTPUT=""
PROPS_JSON=""
PROPS_FILE=""
CONCURRENCY=""
FRAMES=""

# ── Parse arguments ───────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)     PROJECT_DIR="$2";    shift 2 ;;
    --composition) COMPOSITION="$2";    shift 2 ;;
    --quality)     QUALITY="$2";        shift 2 ;;
    --format)      FORMAT="$2";         shift 2 ;;
    --output)      OUTPUT="$2";         shift 2 ;;
    --props)       PROPS_JSON="$2";     shift 2 ;;
    --props-file)  PROPS_FILE="$2";     shift 2 ;;
    --concurrency) CONCURRENCY="$2";    shift 2 ;;
    --frames)      FRAMES="$2";         shift 2 ;;
    --help|-h)
      sed -n '2,30p' "$0" | sed 's/^# //'
      exit 0
      ;;
    *)
      echo "ERROR: Unknown option: $1" >&2
      echo "Run with --help for usage." >&2
      exit 1
      ;;
  esac
done

# ── Validation ────────────────────────────────────────────────────────────────

if [ -z "$COMPOSITION" ]; then
  echo "ERROR: --composition is required." >&2
  echo "Run with --help for usage." >&2
  exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
  echo "ERROR: Project directory not found: $PROJECT_DIR" >&2
  exit 1
fi

if [ ! -f "$PROJECT_DIR/package.json" ]; then
  echo "ERROR: No package.json in $PROJECT_DIR. Is this a Remotion project?" >&2
  exit 1
fi

# Validate quality preset
case "$QUALITY" in
  preview|draft|final|4k) ;;
  *)
    echo "ERROR: Invalid quality preset: $QUALITY" >&2
    echo "Valid options: preview | draft | final | 4k" >&2
    exit 1
    ;;
esac

# Validate format
case "$FORMAT" in
  mp4|webm|gif) ;;
  *)
    echo "ERROR: Invalid format: $FORMAT" >&2
    echo "Valid options: mp4 | webm | gif" >&2
    exit 1
    ;;
esac

# ── Quality preset config ────────────────────────────────────────────────────
#
# Scale is applied as --scale flag to npx remotion render.
# Concurrency is reduced at higher quality to avoid OOM.

case "$QUALITY" in
  preview)
    SCALE="0.25"
    DEFAULT_CONCURRENCY="2"
    QUALITY_LABEL="480p (~25% scale), fast preview"
    ;;
  draft)
    SCALE="0.667"
    DEFAULT_CONCURRENCY="4"
    QUALITY_LABEL="720p (~67% scale), draft review"
    ;;
  final)
    SCALE="1"
    DEFAULT_CONCURRENCY="8"
    QUALITY_LABEL="1080p (full scale), standard delivery"
    ;;
  4k)
    SCALE="2"
    DEFAULT_CONCURRENCY="4"
    QUALITY_LABEL="4K (2x scale), presentation quality"
    ;;
esac

EFFECTIVE_CONCURRENCY="${CONCURRENCY:-$DEFAULT_CONCURRENCY}"

# ── Output path ───────────────────────────────────────────────────────────────

if [ -z "$OUTPUT" ]; then
  OUTPUT_DIR="$PROJECT_DIR/out"
  mkdir -p "$OUTPUT_DIR"
  OUTPUT="$OUTPUT_DIR/${COMPOSITION}.${FORMAT}"
fi

# ── Build command ─────────────────────────────────────────────────────────────

CMD=(npx remotion render
  "$COMPOSITION"
  "$OUTPUT"
  "--scale=$SCALE"
  "--concurrency=$EFFECTIVE_CONCURRENCY"
)

# Format-specific codec
case "$FORMAT" in
  mp4)  CMD+=("--codec=h264") ;;
  webm) CMD+=("--codec=vp8") ;;
  gif)  CMD+=("--codec=gif") ;;
esac

# Props
if [ -n "$PROPS_JSON" ]; then
  CMD+=("--props=$PROPS_JSON")
elif [ -n "$PROPS_FILE" ]; then
  if [ ! -f "$PROPS_FILE" ]; then
    echo "ERROR: Props file not found: $PROPS_FILE" >&2
    exit 1
  fi
  CMD+=("--props=$PROPS_FILE")
fi

# Frame range
if [ -n "$FRAMES" ]; then
  CMD+=("--frames=$FRAMES")
fi

# ── Print render summary ──────────────────────────────────────────────────────

echo "Remotion Render"
echo "  Composition:  $COMPOSITION"
echo "  Quality:      $QUALITY ($QUALITY_LABEL)"
echo "  Format:       $FORMAT"
echo "  Concurrency:  $EFFECTIVE_CONCURRENCY"
echo "  Output:       $OUTPUT"
[ -n "$FRAMES" ] && echo "  Frames:       $FRAMES"
[ -n "$PROPS_JSON" ] && echo "  Props:        $PROPS_JSON"
[ -n "$PROPS_FILE" ] && echo "  Props file:   $PROPS_FILE"
echo ""

# ── Run ───────────────────────────────────────────────────────────────────────

cd "$PROJECT_DIR"

START_TIME=$(date +%s)

"${CMD[@]}"

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

# ── Report ────────────────────────────────────────────────────────────────────

cd - > /dev/null

if [ -f "$OUTPUT" ]; then
  SIZE_BYTES=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT" 2>/dev/null || echo 0)
  SIZE_MB=$(echo "scale=1; $SIZE_BYTES / 1048576" | bc)
  echo ""
  echo "Render complete in ${ELAPSED}s"
  echo "  Output:    $OUTPUT"
  echo "  File size: ${SIZE_MB} MB"
else
  echo ""
  echo "WARNING: Output file not found at expected path: $OUTPUT" >&2
  echo "Check the project's out/ directory for the rendered file." >&2
  exit 1
fi
