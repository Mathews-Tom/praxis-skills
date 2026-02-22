# Design Guide — Concept to Image

Patterns and principles for creating high-quality visuals that don't look AI-generated.

## Layout principles

### Asymmetry over symmetry

Break the grid intentionally. A 60/40 split is more interesting than 50/50. Offset elements. Let one section breathe while another is dense. This creates visual hierarchy naturally.

### Anchor + float

Every visual needs one dominant element (the anchor) that draws the eye first. Other elements float around it with varying proximity. Don't distribute elements evenly — cluster related items and use whitespace to separate groups.

### Edge tension

Let elements approach edges. Bleed graphics to canvas boundaries. This creates energy. A visual where everything is centered with equal margins on all sides looks like a default template.

## Color strategies

### Functional color

Every color should encode meaning — category, importance, state, flow direction. Don't add color for decoration.

```css
/* Example: status encoding */
--c-active: #22c55e; /* green = running/healthy */
--c-warning: #f59e0b; /* amber = degraded */
--c-error: #ef4444; /* red = failed */
--c-neutral: #94a3b8; /* slate = inactive */
```

### Dark-on-light vs light-on-dark

Dark backgrounds (`#1a1a2e`, `#0f172a`) with light text create drama and focus. Light backgrounds (`#f8f6f1`, `#fafaf9`) with dark text feel editorial and clear. Choose based on mood, not default.

### Contrast ratios

Primary text: minimum 7:1 against background. Secondary text: minimum 4.5:1. Decorative elements can be lower contrast.

## Typography patterns

### Scale with purpose

Use a type scale with clear jumps: 10px / 12px / 16px / 24px / 36px / 48px. Don't use sizes that are too close together (14px and 16px side by side reads as an accident).

### Weight as hierarchy

Bold for titles and emphasis. Regular for body. Light/thin for annotations and metadata. Use weight, not just size, to create levels.

### Mono for data

Use monospace fonts for numbers, code, IDs, timestamps — anything that benefits from tabular alignment.

## SVG patterns

### Connectors and flow lines

Use SVG `<path>` with cubic beziers for organic curves, `<line>` for rigid connections. Add arrowhead markers:

```svg
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
    markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--c-primary)"/>
  </marker>
</defs>
<path d="M 100,100 C 200,100 200,200 300,200" stroke="var(--c-primary)"
  fill="none" stroke-width="2" marker-end="url(#arrow)"/>
```

### Icons as inline SVG

Keep icons simple — 24×24 or 32×32 viewBox. Single-color, using `currentColor` so they inherit the parent's text color. Don't use emoji or unicode symbols as icons.

### Gradients and textures

Linear gradients for backgrounds. Radial gradients for spotlight effects. Use SVG `<pattern>` for subtle textures (dots, lines, crosshatch) that add depth without noise.

## Layout patterns by visual type

### Flowchart / Pipeline

- Horizontal flow (left→right) for processes with 3-6 steps
- Vertical flow (top→bottom) for hierarchies or sequences with many steps
- Use SVG for boxes + connectors, CSS Grid for positioning
- Each node: label + optional icon + optional subtitle
- Connector labels for edge descriptions

### Comparison / Matrix

- CSS Grid with explicit column widths
- Header row with category names
- Alternating row backgrounds for readability
- Checkmarks/crosses as inline SVG, not unicode

### Infographic

- Mixed layout: hero stat at top, supporting details in grid below
- Large numbers rendered in display font
- Mini charts as inline SVG (bar charts, donuts)
- Annotation lines connecting data to labels

### Card / Poster

- Typography-dominant: large title, minimal graphics
- Background texture or gradient, not solid flat color
- Content grouped in clear visual blocks
- Generous padding within blocks, tight spacing between related elements

### Pure SVG diagram

- Single root `<svg>` element filling `.canvas`
- All positioning via SVG `transform`, `x`, `y` attributes
- Groups (`<g>`) for logical sections
- Best for: icons, badges, logos, technical diagrams

## Anti-patterns (the "AI slop" checklist)

Avoid all of these:

1. **Centered everything** — Use left-align or asymmetric layouts
2. **Purple gradient hero** — Choose palette with intention
3. **Uniform rounded corners** — Vary radii or use sharp corners; mix both
4. **Equal-width columns** — Use fractional or proportional widths
5. **Shadow on every element** — Use shadow sparingly for elevation hierarchy
6. **Generic placeholder icons** — Draw specific SVG icons for the concept
7. **Over-decoration** — Borders, shadows, gradients AND rounded corners on one element
8. **Low density** — Fill the canvas. 70%+ content-to-whitespace ratio
9. **Orphaned labels** — Every text element should be visually connected to what it describes

## Pre-export checklist

Before running `render_to_image.py`:

- [ ] `.canvas` has explicit `width` and `height` in CSS
- [ ] No external resource references (all inline)
- [ ] Text is readable at export size (check small labels)
- [ ] Colors have sufficient contrast
- [ ] Layout doesn't overflow `.canvas` bounds
- [ ] If SVG export desired: content is inside a root `<svg>` within `.canvas`
