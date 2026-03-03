#!/bin/bash
# scaffold_project.sh — Bootstrap a new Remotion project with TailwindCSS.
#
# Usage:
#   bash scaffold_project.sh [project-name]
#
# Idempotent: detects an existing project and skips re-initialization.
# Requires Node.js 18+.

set -euo pipefail

PROJECT_NAME="${1:-my-remotion-video}"

# ── Preflight ────────────────────────────────────────────────────────────────

if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js is not installed. Install Node.js 18+ from https://nodejs.org" >&2
  exit 1
fi

NODE_VERSION=$(node --version | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  echo "ERROR: Node.js 18+ required. Found: $(node --version)" >&2
  exit 1
fi

if ! command -v npm &>/dev/null; then
  echo "ERROR: npm not found. Install Node.js 18+ from https://nodejs.org" >&2
  exit 1
fi

echo "Node.js: $(node --version)"
echo "npm: $(npm --version)"
echo ""

# ── Idempotency check ────────────────────────────────────────────────────────

if [ -d "$PROJECT_NAME" ] && [ -f "$PROJECT_NAME/package.json" ]; then
  echo "Project '$PROJECT_NAME' already exists. Skipping scaffold."
  echo "To start the preview server:"
  echo "  cd $PROJECT_NAME && npm run dev"
  exit 0
fi

# ── Create Remotion project ──────────────────────────────────────────────────

echo "Creating Remotion project: $PROJECT_NAME"
npx --yes create-video@latest "$PROJECT_NAME" --no-open

cd "$PROJECT_NAME"

# ── Install TailwindCSS and Remotion Tailwind plugin ────────────────────────

echo ""
echo "Installing TailwindCSS..."
npm install tailwindcss @remotion/tailwind

# ── tailwind.config.js ──────────────────────────────────────────────────────

cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
EOF

# ── src/style.css ────────────────────────────────────────────────────────────

mkdir -p src
cat > src/style.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# ── remotion.config.ts — add enableTailwind ──────────────────────────────────

if [ -f "remotion.config.ts" ]; then
  # Patch existing config to add TailwindCSS override
  # Insert import and enableTailwind call if not already present
  if ! grep -q "enableTailwind" remotion.config.ts; then
    cat > remotion.config.ts << 'EOF'
import { Config } from '@remotion/cli/config';
import { enableTailwind } from '@remotion/tailwind';

Config.overrideWebpackConfig((currentConfiguration) => {
  return enableTailwind(currentConfiguration);
});
EOF
    echo "Updated remotion.config.ts with TailwindCSS support."
  fi
else
  cat > remotion.config.ts << 'EOF'
import { Config } from '@remotion/cli/config';
import { enableTailwind } from '@remotion/tailwind';

Config.overrideWebpackConfig((currentConfiguration) => {
  return enableTailwind(currentConfiguration);
});
EOF
  echo "Created remotion.config.ts with TailwindCSS support."
fi

# ── Add style import to Root.tsx ──────────────────────────────────────────────

ROOT_FILE="src/Root.tsx"
if [ -f "$ROOT_FILE" ] && ! grep -q "style.css" "$ROOT_FILE"; then
  # Prepend import to the file
  TMPFILE=$(mktemp)
  echo "import './style.css';" > "$TMPFILE"
  cat "$ROOT_FILE" >> "$TMPFILE"
  mv "$TMPFILE" "$ROOT_FILE"
  echo "Added style.css import to $ROOT_FILE."
fi

# ── public/ directory ────────────────────────────────────────────────────────

mkdir -p public/fonts public/audio public/images

# ── Done ─────────────────────────────────────────────────────────────────────

cd ..

echo ""
echo "Project created: $PROJECT_NAME/"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  npm run dev          # Start Remotion Studio at http://localhost:3000"
echo ""
echo "Render a video:"
echo "  bash ../skills/remotion-video/scripts/render.sh \\"
echo "    --project $PROJECT_NAME \\"
echo "    --composition MyComposition \\"
echo "    --quality final \\"
echo "    --format mp4"
