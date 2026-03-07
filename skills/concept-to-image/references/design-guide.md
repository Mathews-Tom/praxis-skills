# Design Guide — Concept to Image

Patterns and principles for creating high-quality visuals that don't look AI-generated.

## Core philosophy

### Argue, don't display

A visual should make an argument — showing relationships, causality, and flow that text alone can't express. A diagram that just labels boxes is formatted text, not a visual.

**The isomorphism test**: If you removed all text, would the structure alone communicate the concept? If not, the visual design isn't carrying its weight. Redesign until the shapes mirror the meaning.

### Multi-zoom architecture

Comprehensive visuals operate at three levels simultaneously:

1. **Summary flow** — Simplified overview showing the full pipeline at a glance (top or bottom of canvas)
2. **Section boundaries** — Labeled regions that group related components into visual "rooms"
3. **Detail inside sections** — Concrete examples, data formats, code snippets — where the educational value lives

Simple concept cards need only level 1. Technical architecture diagrams need all three.

### Container discipline

Default to no container. Add shapes/boxes only when they carry meaning — grouping, connection endpoints, or semantic shape (decision diamond, etc.). Typography (font size, weight, color) creates hierarchy without boxes.

**The container test**: For each boxed element, ask "Would this work as free-floating text with proper styling?" If yes, remove the box.

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

## Visual pattern library

Match the concept's behavior to the right visual structure. Each major concept in a multi-concept visual should use a **different** pattern — no uniform grids.

| If the concept...            | Pattern                  | HTML/SVG approach                                      |
| ---------------------------- | ------------------------ | ------------------------------------------------------ |
| Spawns multiple outputs      | **Fan-out** (radial)     | Central element + SVG arrows radiating to targets      |
| Combines inputs into one     | **Convergence** (funnel) | Multiple sources + SVG arrows merging to single target |
| Has hierarchy/nesting        | **Tree**                 | Nested containers or SVG lines + positioned labels     |
| Is a sequence of steps       | **Timeline**             | SVG line + dots + labels along the axis                |
| Loops or improves            | **Spiral / Cycle**       | SVG arrows forming a closed loop                       |
| Transforms input to output   | **Assembly line**        | Before → process → after with clear visual contrast    |
| Compares two things          | **Side-by-side**         | CSS Grid parallel columns with visual differentiation  |
| Separates into phases        | **Gap / Break**          | Whitespace or dashed SVG line between sections         |
| Is an abstract state/context | **Cloud**                | Overlapping SVG ellipses with varied sizes             |

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

### Evidence artifacts (for technical diagrams)

When diagramming real systems, include concrete proof — not just labeled boxes:

| Artifact type      | When to use                         | Rendering approach                           |
| ------------------ | ----------------------------------- | -------------------------------------------- |
| Code snippets      | APIs, integrations, implementations | Dark `<pre>` block with syntax-colored spans |
| Data/JSON examples | Schemas, payloads, formats          | Monospace text in a styled container         |
| UI mockups         | Showing actual output               | Nested HTML elements mimicking real UI       |
| Real input content | Showing what goes IN to a system    | Container with sample content visible        |

These raise a diagram from "labeled architecture" to "educational artifact."

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
10. **Displaying instead of arguing** — Boxes with labels connected by arrows. If the structure doesn't mirror the concept's behavior, it's just formatted text
11. **Uniform visual patterns** — Every concept rendered the same way (all rectangles, all cards). Vary patterns per concept
12. **Abstract when concrete is available** — Labeling a box "API Response" instead of showing the actual JSON shape. Use evidence artifacts for technical diagrams

## Pre-export checklist

Before running `render_to_image.py`:

- [ ] `.canvas` has explicit `width` and `height` in CSS
- [ ] No external resource references (all inline)
- [ ] Text is readable at export size (check small labels)
- [ ] Colors have sufficient contrast
- [ ] Layout doesn't overflow `.canvas` bounds
- [ ] If SVG export desired: content is inside a root `<svg>` within `.canvas`
- [ ] Isomorphism test: structure communicates without reading text
- [ ] Each major concept uses a distinct visual pattern (no uniform grid)
- [ ] Technical diagrams include at least one evidence artifact
