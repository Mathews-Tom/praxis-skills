#!/bin/bash
set -e

echo "📦 Validating and finalizing static HTML artifact..."

# Locate the HTML file
HTML_FILE="${1:-index.html}"

if [ ! -f "$HTML_FILE" ]; then
  echo "❌ Error: $HTML_FILE not found."
  echo "   Usage: bash bundle-artifact.sh [filename.html]"
  exit 1
fi

WARNINGS=0

# ── Check for external resource references ──────────────
echo "🔍 Checking self-containment..."

# External stylesheets
EXT_CSS=$(grep -ciE '<link[^>]+rel=["\x27]stylesheet["\x27][^>]+href=["\x27]https?://' "$HTML_FILE" 2>/dev/null || true)
if [ "$EXT_CSS" -gt 0 ] 2>/dev/null; then
  echo "   ⚠  Found $EXT_CSS external stylesheet reference(s) — should be inlined"
  WARNINGS=$((WARNINGS + 1))
fi

# External scripts
EXT_JS=$(grep -ciE '<script[^>]+src=["\x27]https?://' "$HTML_FILE" 2>/dev/null || true)
if [ "$EXT_JS" -gt 0 ] 2>/dev/null; then
  echo "   ⚠  Found $EXT_JS external script reference(s) — should be inlined"
  WARNINGS=$((WARNINGS + 1))
fi

# External images
EXT_IMG=$(grep -ciE '<img[^>]+src=["\x27]https?://' "$HTML_FILE" 2>/dev/null || true)
if [ "$EXT_IMG" -gt 0 ] 2>/dev/null; then
  echo "   ⚠  Found $EXT_IMG external image reference(s) — use inline SVG or data URIs"
  WARNINGS=$((WARNINGS + 1))
fi

# External fonts (Google Fonts, etc.)
EXT_FONT=$(grep -ciE 'fonts\.googleapis\.com|fonts\.gstatic\.com' "$HTML_FILE" 2>/dev/null || true)
if [ "$EXT_FONT" -gt 0 ] 2>/dev/null; then
  echo "   ⚠  Found external font reference(s) — use system font stack for self-containment"
  WARNINGS=$((WARNINGS + 1))
fi

if [ "$WARNINGS" -eq 0 ]; then
  echo "   ✅ Fully self-contained — no external dependencies"
fi

# ── Check for inline SVG presence ───────────────────────
echo "🔍 Checking iconography..."
SVG_COUNT=$(grep -co '<svg' "$HTML_FILE" 2>/dev/null || echo "0")
echo "   Found $SVG_COUNT inline SVG element(s)"
if [ "$SVG_COUNT" -eq 0 ]; then
  echo "   ⚠  No inline SVGs found — infographics should include SVG icons"
  WARNINGS=$((WARNINGS + 1))
fi

# ── Check for CSS Grid / Flexbox usage ──────────────────
echo "🔍 Checking layout system..."
HAS_GRID=$(grep -c 'display:\s*grid\|display: grid' "$HTML_FILE" 2>/dev/null || echo "0")
HAS_FLEX=$(grep -c 'display:\s*flex\|display: flex' "$HTML_FILE" 2>/dev/null || echo "0")
echo "   Grid declarations: $HAS_GRID | Flex declarations: $HAS_FLEX"

# ── Copy to bundle.html ────────────────────────────────
cp "$HTML_FILE" bundle.html

# ── Report ──────────────────────────────────────────────
FILE_SIZE=$(du -h bundle.html | cut -f1)
LINE_COUNT=$(wc -l < bundle.html)

echo ""
if [ "$WARNINGS" -gt 0 ]; then
  echo "⚠  Finalized with $WARNINGS warning(s)"
else
  echo "✅ Finalized cleanly"
fi
echo "📄 Output: bundle.html ($FILE_SIZE, $LINE_COUNT lines)"
echo ""
echo "You can now use this single HTML file as an artifact in Claude conversations."
