# Theme Reference

This file contains the complete CSS variable definitions and base styles for each supported theme. When generating a presentation, copy the CSS for the selected theme into the `<style>` block of the HTML file.

## Table of Contents

1. [dark-editorial](#dark-editorial) — Dark background, serif headlines, editorial magazine feel
2. [light-minimal](#light-minimal) — Clean white background, geometric sans-serif, airy spacing
3. [corporate](#corporate) — Navy and white, professional, boardroom-ready
4. [hacker](#hacker) — Terminal green on black, monospace everything, raw/brutalist

---

## dark-editorial

Inspired by high-end editorial design. Dark background with subtle grid texture, serif italic headlines, steel-blue accents. Best for: conference talks, technical deep-dives, product launches.

```css
:root {
  --bg-dark: #0a0a0a;
  --bg-card: #111111;
  --bg-card-hover: #1a1a1a;
  --accent: #7b8fa8;
  --accent-light: #9bb0c9;
  --accent-glow: rgba(123, 143, 168, 0.15);
  --success: #7b9a7b;
  --warning: #c9a85b;
  --error: #c97b7b;
  --text-primary: #f5f4f0;
  --text-secondary: #a8a8a8;
  --text-muted: #666666;
  --border: #2a2a2a;
  --font-serif: "Playfair Display", Georgia, serif;
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: "JetBrains Mono", monospace;
}
```

**Google Fonts import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap"
  rel="stylesheet"
/>
```

**Background treatment:**

```css
.reveal-viewport,
.presentation-viewport {
  background: var(--bg-dark) !important;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px) !important;
  background-size: 60px 60px !important;
}
```

**Typography:**

```css
h1,
.h1 {
  font-family: var(--font-serif);
  font-size: 3.5rem;
  font-weight: 400;
  font-style: italic;
  line-height: 1.1;
  color: var(--text-primary);
}

h2,
.h2 {
  font-family: var(--font-serif);
  font-size: 2.5rem;
  font-weight: 400;
  line-height: 1.15;
}

h3,
.h3 {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 400;
  line-height: 1.3;
}

h4,
.h4 {
  font-family: var(--font-sans);
  font-size: 1.1rem;
  font-weight: 500;
  letter-spacing: 0.02em;
}
```

**Section slide glow effect:**

```css
.slide--section::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}
```

---

## light-minimal

Clean, modern, airy. White space is a feature. Best for: internal reports, educational content, documentation presentations.

```css
:root {
  --bg-dark: #fafafa;
  --bg-card: #ffffff;
  --bg-card-hover: #f0f0f0;
  --accent: #2563eb;
  --accent-light: #3b82f6;
  --accent-glow: rgba(37, 99, 235, 0.08);
  --success: #16a34a;
  --warning: #d97706;
  --error: #dc2626;
  --text-primary: #111827;
  --text-secondary: #4b5563;
  --text-muted: #9ca3af;
  --border: #e5e7eb;
  --font-serif: "Libre Baskerville", Georgia, serif;
  --font-sans: "DM Sans", -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: "IBM Plex Mono", monospace;
}
```

**Google Fonts import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap"
  rel="stylesheet"
/>
```

**Background treatment:**

```css
.reveal-viewport,
.presentation-viewport {
  background: var(--bg-dark) !important;
}
```

**Typography — no italic headlines, clean geometric feel:**

```css
h1,
.h1 {
  font-family: var(--font-sans);
  font-size: 3.5rem;
  font-weight: 700;
  font-style: normal;
  line-height: 1.1;
  color: var(--text-primary);
}

h2,
.h2 {
  font-family: var(--font-sans);
  font-size: 2.5rem;
  font-weight: 600;
  line-height: 1.15;
}
```

**Card style — elevated with shadow instead of border:**

```css
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: var(--spacing-md);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
```

---

## corporate

Boardroom-ready. Navy backgrounds with white panels. Confident, authoritative. Best for: investor pitches, executive presentations, client proposals.

```css
:root {
  --bg-dark: #0f172a;
  --bg-card: #1e293b;
  --bg-card-hover: #334155;
  --accent: #f59e0b;
  --accent-light: #fbbf24;
  --accent-glow: rgba(245, 158, 11, 0.12);
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --border: #334155;
  --font-serif: "Merriweather", Georgia, serif;
  --font-sans: "Source Sans 3", -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: "Source Code Pro", monospace;
}
```

**Google Fonts import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;1,400&family=Source+Code+Pro:wght@400;500&family=Source+Sans+3:wght@300;400;500;600;700&display=swap"
  rel="stylesheet"
/>
```

**Background — clean navy, no grid texture:**

```css
.reveal-viewport,
.presentation-viewport {
  background: var(--bg-dark) !important;
}
```

**Typography — bold sans headlines, gold accent underlines:**

```css
h1,
.h1 {
  font-family: var(--font-sans);
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  color: var(--text-primary);
}

h2,
.h2 {
  font-family: var(--font-sans);
  font-size: 2.5rem;
  font-weight: 600;
  line-height: 1.15;
}

/* Optional: gold underline on h2 */
h2::after {
  content: "";
  display: block;
  width: 60px;
  height: 3px;
  background: var(--accent);
  margin-top: 12px;
}
```

---

## hacker

Terminal aesthetic. Green phosphor on black. Monospace everything. Raw, technical, no-nonsense. Best for: dev talks, security presentations, technical demos, CTF walkthroughs.

```css
:root {
  --bg-dark: #0a0a0a;
  --bg-card: #0f0f0f;
  --bg-card-hover: #1a1a1a;
  --accent: #00ff88;
  --accent-light: #33ffaa;
  --accent-glow: rgba(0, 255, 136, 0.08);
  --success: #00ff88;
  --warning: #ffcc00;
  --error: #ff4444;
  --text-primary: #00ff88;
  --text-secondary: #00cc66;
  --text-muted: #336644;
  --border: #1a3322;
  --font-serif: "IBM Plex Mono", monospace;
  --font-sans: "IBM Plex Mono", monospace;
  --font-mono: "IBM Plex Mono", monospace;
}
```

**Google Fonts import:**

```html
<link
  href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap"
  rel="stylesheet"
/>
```

**Background — scanline effect:**

```css
.reveal-viewport,
.presentation-viewport {
  background: var(--bg-dark) !important;
  background-image: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 255, 136, 0.03) 2px,
    rgba(0, 255, 136, 0.03) 4px
  ) !important;
}
```

**Typography — all monospace, no serif distinction:**

```css
h1,
.h1 {
  font-family: var(--font-mono);
  font-size: 3rem;
  font-weight: 600;
  font-style: normal;
  line-height: 1.1;
  color: var(--accent);
  text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
}

h2,
.h2 {
  font-family: var(--font-mono);
  font-size: 2rem;
  font-weight: 500;
  line-height: 1.2;
  color: var(--accent);
}

/* Kicker uses > prefix like terminal prompt */
.kicker::before {
  content: "> ";
  color: var(--accent);
}

.kicker::after {
  content: "_";
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}
```

**Card style — dashed borders, terminal feel:**

```css
.card {
  border: 1px dashed var(--border);
  background: transparent;
}

.card:hover {
  border-color: var(--accent);
  box-shadow: 0 0 10px rgba(0, 255, 136, 0.1);
}
```

---

## Common Styles (All Themes)

These styles are shared across all themes. Include them after the theme-specific CSS.

```css
/* === SPACING === */
:root {
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 40px;
  --spacing-xl: 60px;
}

/* === BASE RESET === */
html,
body {
  background: var(--bg-dark) !important;
  color: var(--text-primary);
  margin: 0;
  height: 100%;
}

body {
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
}

/* === SLIDE STRUCTURE === */
.slide {
  height: 100%;
  width: 100%;
  padding: var(--spacing-xl);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  background: transparent;
  position: relative;
}

.slide > * {
  position: relative;
  z-index: 1;
}
.slide--center {
  align-items: center;
  justify-content: center;
  text-align: center;
}

/* === HEADER === */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.header__logo {
  font-family: var(--font-serif);
  font-size: 0.9rem;
  font-weight: 400;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 10px;
  letter-spacing: 0.02em;
}

.header__logo svg {
  width: 18px;
  height: 18px;
  color: var(--accent);
}

/* === KICKER === */
.kicker {
  font-size: 0.7rem;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.25em;
  margin-bottom: var(--spacing-sm);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
}

.kicker::after {
  content: "";
  width: 40px;
  height: 1px;
  background: var(--accent);
  opacity: 0.5;
}

/* === LEAD TEXT === */
.lead {
  font-size: 1.1rem;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 600px;
}

/* === TEXT UTILITIES === */
.muted {
  color: var(--text-muted);
}
.highlight,
.accent-text {
  color: var(--accent);
}

/* === CODE === */
code,
.code {
  font-family: var(--font-mono);
  background: rgba(123, 143, 168, 0.1);
  padding: 2px 8px;
  font-size: 0.85em;
  color: var(--accent-light);
  border: 1px solid var(--border);
}

pre {
  background: #0d0d0d;
  border: 1px solid var(--border);
  padding: var(--spacing-md);
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 0.75em;
  line-height: 1.6;
}

pre code {
  background: none;
  padding: 0;
  border: none;
  color: var(--text-secondary);
}

/* === LAYOUT HELPERS === */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
  align-items: center;
  flex: 1;
}
.split--60-40 {
  grid-template-columns: 1.5fr 1fr;
}
.split--40-60 {
  grid-template-columns: 1fr 1.5fr;
}
.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}
.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
}
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* === CARDS === */
.card {
  background: transparent;
  border: 1px solid var(--border);
  padding: var(--spacing-md);
  transition: all 0.3s ease;
}

.card:hover {
  background: var(--bg-card);
  border-color: var(--accent);
}
.card--featured {
  border-color: var(--accent);
}
.card--danger {
  border-color: var(--error);
}
.card--success {
  border-color: var(--success);
}
.card--warning {
  border-color: var(--warning);
}

.card__icon {
  width: 40px;
  height: 40px;
  margin-bottom: var(--spacing-sm);
  color: var(--accent);
}
.card__icon svg {
  width: 100%;
  height: 100%;
  stroke-width: 1.5;
}
.card__icon--danger {
  color: var(--error);
}
.card__icon--success {
  color: var(--success);
}
.card__title {
  font-family: var(--font-sans);
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: var(--spacing-xs);
}
.card__text {
  font-size: 0.9rem;
  color: var(--text-muted);
  line-height: 1.5;
}

/* === METRICS === */
.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
}
.metric {
  text-align: center;
  padding: var(--spacing-md);
  border: 1px solid var(--border);
  transition: all 0.3s ease;
}
.metric:hover {
  border-color: var(--accent);
}
.metric--danger {
  border-color: var(--error);
}
.metric--danger .metric__value {
  color: var(--error);
}
.metric__value {
  font-family: var(--font-serif);
  font-size: 2.5rem;
  font-weight: 400;
  font-style: italic;
  color: var(--accent);
  line-height: 1;
  margin-bottom: var(--spacing-xs);
}
.metric__label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* === LISTS === */
.list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.list li {
  padding: var(--spacing-sm) 0;
  padding-left: var(--spacing-lg);
  position: relative;
  border-bottom: 1px solid var(--border);
}
.list li:last-child {
  border-bottom: none;
}
.list li::before {
  content: "—";
  position: absolute;
  left: 0;
  top: var(--spacing-sm);
  color: var(--accent);
}
.list--check li::before {
  content: "✓";
  color: var(--success);
}
.list--x li::before {
  content: "✗";
  color: var(--error);
}
.list--numbered {
  counter-reset: list-counter;
}
.list--numbered li {
  counter-increment: list-counter;
}
.list--numbered li::before {
  content: counter(list-counter, decimal-leading-zero);
  color: var(--accent);
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.05em;
}

/* === BADGES === */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  font-size: 0.7rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
}
.badge--success {
  color: var(--success);
  border-color: var(--success);
}
.badge--warning {
  color: var(--warning);
  border-color: var(--warning);
}
.badge--danger {
  color: var(--error);
  border-color: var(--error);
}

/* === QUOTES === */
.quote-block {
  border-left: 3px solid var(--accent);
  padding-left: var(--spacing-md);
  font-style: italic;
  color: var(--text-secondary);
}
.quote-author {
  margin-top: var(--spacing-sm);
  font-style: normal;
  font-size: 0.85rem;
  color: var(--text-muted);
}

/* === COMPARISON TABLE === */
.comparison-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: var(--spacing-md);
}
.comparison-table th,
.comparison-table td {
  padding: var(--spacing-sm);
  text-align: left;
  border-bottom: 1px solid var(--border);
  font-size: 0.9rem;
}
.comparison-table th {
  color: var(--text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.7rem;
}
.check {
  color: var(--success);
}
.cross {
  color: var(--error);
}

/* === WORKFLOW === */
.workflow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}
.workflow__step {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.workflow__box {
  border: 1px solid var(--border);
  padding: var(--spacing-sm) var(--spacing-md);
  text-align: center;
  min-width: 120px;
}
.workflow__label {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent-light);
}
.workflow__sublabel {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-top: 4px;
}
.workflow__arrow {
  color: var(--accent);
  font-size: 1.5rem;
}

/* === TIMELINE === */
.timeline {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: var(--spacing-lg) 0;
  position: relative;
}
.timeline::before {
  content: "";
  position: absolute;
  bottom: 60px;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--border);
}
.timeline__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  flex: 1;
}
.timeline__year {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  font-style: italic;
  color: var(--accent);
  margin-bottom: var(--spacing-sm);
}
.timeline__dot {
  width: 10px;
  height: 10px;
  background: var(--accent);
  border-radius: 50%;
  margin-bottom: var(--spacing-sm);
  position: relative;
  z-index: 1;
}
.timeline__content {
  font-size: 0.85rem;
  color: var(--text-secondary);
  max-width: 150px;
}

/* === CONTACT GRID === */
.contact-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-lg);
  margin-top: var(--spacing-xl);
}
.contact-item {
  text-align: center;
}
.contact-item__label {
  font-size: 0.7rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: var(--spacing-xs);
}
.contact-item__value {
  font-size: 0.95rem;
  color: var(--text-secondary);
}

/* === BUTTONS === */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 28px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--text-primary);
  background: transparent;
  color: var(--text-primary);
}
.btn:hover {
  background: var(--text-primary);
  color: var(--bg-dark);
}
.btn--accent {
  border-color: var(--accent);
  color: var(--accent);
}
.btn--accent:hover {
  background: var(--accent);
  color: var(--bg-dark);
}

/* === RESPONSIVE === */
@media (max-width: 1400px) {
  h1 {
    font-size: 3rem;
  }
  h2 {
    font-size: 2.2rem;
  }
  .slide {
    padding: var(--spacing-lg);
  }
}

@media (max-width: 1024px) {
  h1 {
    font-size: 2.5rem;
  }
  h2 {
    font-size: 1.8rem;
  }
  .lead {
    font-size: 1rem;
  }
  .split {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  .grid-4,
  .grid-3 {
    grid-template-columns: repeat(2, 1fr);
  }
  .workflow {
    flex-wrap: wrap;
  }
  .metrics {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  h2 {
    font-size: 1.5rem;
  }
  .slide {
    padding: var(--spacing-md);
  }
  .grid-2,
  .grid-3,
  .grid-4 {
    grid-template-columns: 1fr;
  }
  .contact-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  .metrics {
    grid-template-columns: 1fr;
  }
}
```

### Reveal.js Overrides (Horizontal Mode Only)

Include these when using Reveal.js:

```css
.reveal {
  background: var(--bg-dark);
  font-family: var(--font-sans);
  font-size: 22px;
  color: var(--text-primary);
}
.reveal .slides {
  text-align: left;
}
.reveal .slides section {
  padding: 0;
  background: var(--bg-dark);
}
.reveal .controls {
  color: var(--accent);
}
.reveal .progress {
  background: var(--border);
  height: 2px;
}
.reveal .progress span {
  background: var(--accent);
}
.reveal .slide-number {
  background: transparent;
  color: var(--text-muted);
  font-size: 12px;
  font-family: var(--font-mono);
  right: 20px;
  bottom: 20px;
}
.reveal .slides section .fragment {
  opacity: 0;
  transition: all 0.4s ease;
}
.reveal .slides section .fragment.visible {
  opacity: 1;
}
.reveal .slides section .fragment.fade-up {
  transform: translateY(20px);
}
.reveal .slides section .fragment.fade-up.visible {
  transform: translateY(0);
}

/* Ensure links are clickable */
.reveal a.btn,
.reveal [data-prevent-swipe],
.reveal [data-prevent-swipe] * {
  pointer-events: auto !important;
  position: relative;
  z-index: 9999 !important;
  cursor: pointer !important;
}
.reveal .slides section * {
  pointer-events: auto;
}
```
