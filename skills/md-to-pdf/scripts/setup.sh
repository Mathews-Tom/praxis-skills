#!/usr/bin/env bash
# setup.sh — Verify (and optionally install) dependencies for md-to-pdf skill
#
# Usage:
#   bash setup.sh           # Check only
#   bash setup.sh --install # Check and install missing deps
#
# Exit codes: 0 = all OK, 1 = missing deps (without --install)

set -euo pipefail

INSTALL="${1:-}"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
FAIL=0

ok()   { printf "${GREEN}✓${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}⚠${NC} %s\n" "$1"; }
fail() { printf "${RED}✗${NC} %s\n" "$1"; FAIL=1; }

echo "=== md-to-pdf dependency check ==="
echo ""

# --- pandoc ---
if command -v pandoc &>/dev/null; then
    ok "pandoc $(pandoc --version | head -1 | awk '{print $2}')"
elif [[ "$INSTALL" == "--install" ]]; then
    warn "pandoc not found — installing..."
    sudo apt-get update -qq && sudo apt-get install -y -qq pandoc
    ok "pandoc installed"
else
    fail "pandoc not found (apt install pandoc)"
fi

# --- Node.js ---
if command -v node &>/dev/null; then
    ok "node $(node --version)"
else
    fail "node not found — required for KaTeX and Mermaid"
fi

# --- mmdc (mermaid-cli) ---
if command -v mmdc &>/dev/null; then
    ok "mmdc (mermaid-cli) $(mmdc --version 2>/dev/null || echo 'unknown')"
elif [[ "$INSTALL" == "--install" ]]; then
    warn "mmdc not found — installing @mermaid-js/mermaid-cli..."
    npm install -g @mermaid-js/mermaid-cli
    ok "mmdc installed"
else
    fail "mmdc not found (npm install -g @mermaid-js/mermaid-cli)"
fi

# --- KaTeX (npm) ---
if node -e "require('katex')" 2>/dev/null; then
    KATEX_VER=$(node -e "console.log(require('katex').version || 'loaded')" 2>/dev/null)
    ok "katex $KATEX_VER"
elif [[ "$INSTALL" == "--install" ]]; then
    warn "katex not found — installing..."
    npm install -g katex
    ok "katex installed"
else
    fail "katex not found (npm install -g katex)"
fi

# --- Playwright (Python) ---
if python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    PW_VER=$(python3 -c "import playwright; print(playwright.__version__)" 2>/dev/null || echo "unknown")
    ok "playwright (Python) $PW_VER"
elif [[ "$INSTALL" == "--install" ]]; then
    warn "playwright not found — installing..."
    pip install playwright --break-system-packages 2>/dev/null || pip install playwright
    playwright install chromium
    ok "playwright installed"
else
    fail "playwright not found (pip install playwright && playwright install chromium)"
fi

# --- Chrome/Chromium binary ---
CHROME_FOUND=0
for candidate in \
    "$HOME/.cache/puppeteer/chrome" \
    "/opt/google/chrome/chrome" \
    "/opt/pw-browsers" \
    "$HOME/.cache/ms-playwright"; do
    if [[ -d "$candidate" ]]; then
        CHROME_BIN=$(find "$candidate" -name "chrome" -type f -perm /u+x 2>/dev/null | head -1)
        if [[ -n "$CHROME_BIN" ]]; then
            ok "Chrome binary: $CHROME_BIN"
            CHROME_FOUND=1
            break
        fi
    elif [[ -x "$candidate" ]]; then
        ok "Chrome binary: $candidate"
        CHROME_FOUND=1
        break
    fi
done

for sys_chrome in /usr/bin/chromium-browser /usr/bin/chromium /usr/bin/google-chrome; do
    if [[ $CHROME_FOUND -eq 0 && -x "$sys_chrome" ]]; then
        ok "Chrome binary: $sys_chrome"
        CHROME_FOUND=1
        break
    fi
done

if [[ $CHROME_FOUND -eq 0 ]]; then
    fail "No Chrome/Chromium binary found (playwright install chromium)"
fi

# --- KaTeX CSS + fonts ---
KATEX_DIR=$(node -e "try{console.log(require.resolve('katex').replace(/katex\\.js$/,''))}catch(e){}" 2>/dev/null)
if [[ -n "$KATEX_DIR" && -f "${KATEX_DIR}katex.min.css" && -d "${KATEX_DIR}fonts" ]]; then
    FONT_COUNT=$(ls "${KATEX_DIR}fonts/" 2>/dev/null | wc -l)
    ok "KaTeX CSS + fonts ($FONT_COUNT font files)"
else
    warn "KaTeX CSS/fonts not found — math will render but may look degraded"
fi

# --- Summary ---
echo ""
if [[ $FAIL -eq 0 ]]; then
    echo -e "${GREEN}All dependencies satisfied.${NC} Ready to convert."
    exit 0
else
    echo -e "${RED}Missing dependencies detected.${NC} Run: bash setup.sh --install"
    exit 1
fi
