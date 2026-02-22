#!/bin/bash

# Exit on error
set -e

# Check if project name is provided
if [ -z "$1" ]; then
  echo "❌ Usage: ./init-artifact.sh <project-name>"
  exit 1
fi

PROJECT_NAME="$1"

echo "🚀 Creating new static infographic project: $PROJECT_NAME"

# Create project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Create the template HTML
echo "📝 Generating scaffold HTML with CSS Grid layout system..."
cat > index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Infographic</title>
  <style>
    /* ── Reset ─────────────────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* ── Palette (CSS Custom Properties) ───────────────── */
    :root {
      --color-bg:        #FAFBFC;
      --color-surface:   #FFFFFF;
      --color-border:    #D0D7DE;

      --color-primary:   #0969DA;
      --color-secondary: #1A7F37;
      --color-accent:    #BF3989;
      --color-neutral:   #656D76;

      --color-text:      #1F2328;
      --color-text-muted:#656D76;

      --shadow-sm: 0 1px 2px rgba(31,35,40,0.06);
      --shadow-md: 0 3px 8px rgba(31,35,40,0.12);
      --shadow-lg: 0 8px 24px rgba(31,35,40,0.16);

      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 12px;

      --gap-xs: 4px;
      --gap-sm: 8px;
      --gap-md: 16px;
      --gap-lg: 24px;
      --gap-xl: 32px;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      font-size: 14px;
      line-height: 1.5;
      color: var(--color-text);
      background: var(--color-bg);
    }

    /* ── Page Container ────────────────────────────────── */
    .page {
      max-width: 1200px;
      margin: 0 auto;
      padding: var(--gap-lg);
    }

    /* ── Grid Utilities ────────────────────────────────── */
    .grid        { display: grid; gap: var(--gap-md); }
    .grid-2      { grid-template-columns: repeat(2, 1fr); }
    .grid-3      { grid-template-columns: repeat(3, 1fr); }
    .grid-4      { grid-template-columns: repeat(4, 1fr); }
    .grid-sidebar{ grid-template-columns: 280px 1fr; }
    .grid-holy   { grid-template-columns: 200px 1fr 200px; }

    /* ── Flex Utilities ────────────────────────────────── */
    .flex        { display: flex; }
    .flex-col    { flex-direction: column; }
    .flex-center { align-items: center; justify-content: center; }
    .flex-between{ justify-content: space-between; }
    .flex-wrap   { flex-wrap: wrap; }
    .gap-xs      { gap: var(--gap-xs); }
    .gap-sm      { gap: var(--gap-sm); }
    .gap-md      { gap: var(--gap-md); }
    .gap-lg      { gap: var(--gap-lg); }
    .gap-xl      { gap: var(--gap-xl); }

    /* ── Card / Surface ────────────────────────────────── */
    .card {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      padding: var(--gap-md);
      box-shadow: var(--shadow-sm);
    }
    .card-elevated {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      padding: var(--gap-md);
      box-shadow: var(--shadow-md);
    }

    /* ── Badge / Tag ───────────────────────────────────── */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: var(--gap-xs);
      padding: 2px 8px;
      font-size: 12px;
      font-weight: 500;
      border-radius: 9999px;
      background: var(--color-primary);
      color: #fff;
    }
    .badge-secondary { background: var(--color-secondary); }
    .badge-accent    { background: var(--color-accent); }
    .badge-neutral   { background: var(--color-neutral); }

    /* ── Typography ────────────────────────────────────── */
    .title    { font-size: 28px; font-weight: 700; line-height: 1.2; }
    .subtitle { font-size: 18px; font-weight: 600; line-height: 1.3; }
    .caption  { font-size: 12px; color: var(--color-text-muted); }
    .mono     { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; }

    /* ── Icon container (for inline SVG) ───────────────── */
    .icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 20px;
      height: 20px;
      flex-shrink: 0;
    }
    .icon svg { width: 100%; height: 100%; }
    .icon-lg  { width: 32px; height: 32px; }
    .icon-xl  { width: 48px; height: 48px; }

    /* ── Connector Lines (SVG overlay pattern) ─────────── */
    .connector-layer {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 1;
    }
    .connector-layer svg { width: 100%; height: 100%; }

    /* ── Section Divider ───────────────────────────────── */
    .divider {
      border: none;
      border-top: 1px solid var(--color-border);
      margin: var(--gap-md) 0;
    }

    /* ── Tier / Layer Band ─────────────────────────────── */
    .tier {
      padding: var(--gap-md) var(--gap-lg);
      border-radius: var(--radius-md);
      position: relative;
    }
    .tier-primary   { background: rgba(9,105,218,0.06); border-left: 3px solid var(--color-primary); }
    .tier-secondary { background: rgba(26,127,55,0.06); border-left: 3px solid var(--color-secondary); }
    .tier-accent    { background: rgba(191,57,137,0.06); border-left: 3px solid var(--color-accent); }
    .tier-neutral   { background: rgba(101,109,118,0.06); border-left: 3px solid var(--color-neutral); }
  </style>
</head>
<body>

  <div class="page">
    <!-- ═══ HEADER ═══════════════════════════════════════ -->
    <header class="flex flex-col gap-sm" style="margin-bottom: var(--gap-lg);">
      <h1 class="title">Infographic Title</h1>
      <p class="caption">Subtitle or context line</p>
    </header>

    <!-- ═══ MAIN GRID ════════════════════════════════════ -->
    <div class="grid grid-3 gap-lg">
      <div class="card">
        <div class="flex gap-sm" style="align-items: center; margin-bottom: var(--gap-sm);">
          <span class="icon icon-lg" style="color: var(--color-primary);">
            <!-- inline SVG icon here -->
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/></svg>
          </span>
          <span class="subtitle">Section A</span>
        </div>
        <p>Content block with intentional padding and grid placement.</p>
      </div>

      <div class="card">
        <div class="flex gap-sm" style="align-items: center; margin-bottom: var(--gap-sm);">
          <span class="icon icon-lg" style="color: var(--color-secondary);">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
          </span>
          <span class="subtitle">Section B</span>
        </div>
        <p>Content block with intentional padding and grid placement.</p>
      </div>

      <div class="card">
        <div class="flex gap-sm" style="align-items: center; margin-bottom: var(--gap-sm);">
          <span class="icon icon-lg" style="color: var(--color-accent);">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"/></svg>
          </span>
          <span class="subtitle">Section C</span>
        </div>
        <p>Content block with intentional padding and grid placement.</p>
      </div>
    </div>
  </div>

</body>
</html>
HTMLEOF

echo ""
echo "✅ Scaffold complete!"
echo ""
echo "📁 Created:"
echo "   $PROJECT_NAME/"
echo "   └── index.html  (template with CSS Grid layout system + CSS custom properties)"
echo ""
echo "CSS utilities available:"
echo "  Layout:  .grid, .grid-2, .grid-3, .grid-4, .grid-sidebar, .grid-holy"
echo "  Flex:    .flex, .flex-col, .flex-center, .flex-between, .flex-wrap"
echo "  Gaps:    .gap-xs, .gap-sm, .gap-md, .gap-lg, .gap-xl"
echo "  Surface: .card, .card-elevated"
echo "  Tiers:   .tier-primary, .tier-secondary, .tier-accent, .tier-neutral"
echo "  Badges:  .badge, .badge-secondary, .badge-accent, .badge-neutral"
echo "  Type:    .title, .subtitle, .caption, .mono"
echo "  Icons:   .icon, .icon-lg, .icon-xl"
echo ""
echo "To develop: edit $PROJECT_NAME/index.html directly. No build step required."
