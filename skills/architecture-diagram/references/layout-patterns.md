# Layout Patterns

## Node structure

Every node has three text slots:

```html
<div class="node" data-node-id="unique-id">
  <div class="node-icon"><!-- inline SVG --></div>
  <span class="node-title">Short Name</span>
  <span class="node-desc"
    >Extended description, capabilities, protocols, etc.</span
  >
</div>
```

- `node-title`: bold 12px, 1-3 words. Always present.
- `node-desc`: light 10.5px, multi-line. Optional but strongly recommended for nodes with rich context (protocol lists, service details, module names).

## Zone nesting

Every zone = `div.zone.zone-depth-N` > `span.zone-label` + `div.zone-content`.

Zone depth class drives border color, bg opacity, label color via CSS custom properties. Depths 0–3 predefined; deeper nesting: set `--zone-border`, `--zone-bg`, `--zone-label-color`, `--zone-label-bg` inline.

Every `.zone-content` must have explicit `style="grid-template-columns: ..."`.

## Topology patterns

### Three-column integration flow (left → center → right)

Primary pattern for source→platform→target architectures. Left/right columns hold vertically-stacked nodes. Center holds the integration platform with nested zones.

**Critical layout rules:**

- Outer grid: `align-items: start` — each zone sizes to its own content. Never use `stretch` which forces equal heights and creates dead space.
- Side column interiors: `align-content: space-evenly` — distributes nodes evenly across the zone's natural height, preventing top-clustering.
- Side columns use fixed widths (180–240px). Center uses `1fr`.

```html
<div
  class="zone-content"
  style="grid-template-columns: 210px 1fr 200px; gap: 28px; align-items: start;"
>
  <!-- LEFT: Source Systems -->
  <div class="zone zone-depth-0">
    <span class="zone-label">Source Systems</span>
    <div
      class="zone-content"
      style="grid-template-columns: 1fr; gap: 24px; justify-items: center;"
    >
      <div class="node" data-node-id="src-1">...</div>
      <div class="node" data-node-id="src-2">...</div>
      <div class="node" data-node-id="src-3">...</div>
    </div>
  </div>

  <!-- CENTER: Integration Platform -->
  <div class="zone zone-depth-0">
    <span class="zone-label">Platform</span>
    <div class="zone-content" style="grid-template-columns: 1fr;">
      <!-- nested zones: Compartments → VCN → Subnet → service grid -->
    </div>
  </div>

  <!-- RIGHT: Target Systems -->
  <div class="zone zone-depth-0">
    <span class="zone-label">Target Systems</span>
    <div
      class="zone-content"
      style="grid-template-columns: 1fr; gap: 16px; justify-items: center;"
    >
      <div class="node" data-node-id="tgt-1">...</div>
      <div class="node" data-node-id="tgt-2">...</div>
    </div>
  </div>
</div>
```

**Column sizing heuristics:**

- Source/target side columns: 180–240px (enough for icon + description text)
- Center platform: `1fr` (takes remaining space)
- When center has deep nesting (4+ levels), widen to `minmax(500px, 1fr)`
- Outer gap: 24–32px between the three columns

### Two-column split (on-prem ↔ cloud)

```html
<div class="zone-content" style="grid-template-columns: 1fr 1fr; gap: 24px;">
  <div class="zone zone-depth-0"><!-- left --></div>
  <div class="zone zone-depth-0"><!-- right --></div>
</div>
```

### Region → VPC → Subnet (pure cloud)

```html
<div class="zone zone-depth-0">
  <span class="zone-label">Region</span>
  <div class="zone-content" style="grid-template-columns: 1fr;">
    <div class="zone zone-depth-1">
      <span class="zone-label">VPC</span>
      <div class="zone-content" style="grid-template-columns: 1fr 1fr;">
        <div class="zone zone-depth-2">
          <span class="zone-label">Public Subnet</span>...
        </div>
        <div class="zone zone-depth-2">
          <span class="zone-label">Private Subnet</span>...
        </div>
      </div>
    </div>
  </div>
</div>
```

### Hub-and-spoke

```html
<div
  class="zone-content"
  style="grid-template-columns: 1fr auto 1fr; gap: 20px;"
>
  <div class="zone zone-depth-1"><!-- left --></div>
  <div class="node" data-node-id="hub"><!-- central --></div>
  <div class="zone zone-depth-1"><!-- right --></div>
</div>
```

### Vertical tier stack

```html
<div class="zone-content" style="grid-template-columns: 1fr; gap: 18px;">
  <div class="zone zone-depth-1">
    <span class="zone-label">Presentation</span>...
  </div>
  <div class="zone zone-depth-1">
    <span class="zone-label">Application</span>...
  </div>
  <div class="zone zone-depth-1"><span class="zone-label">Data</span>...</div>
</div>
```

## Platform interior grid

Inside the innermost zone (e.g., Subnet), service nodes typically arrange in a 2-column grid:

```html
<div class="zone-content" style="grid-template-columns: 1fr 1fr; gap: 20px;">
  <!-- Row 1 -->
  <div class="node">Event Layer</div>
  <div class="node">Integration Engine</div>
  <!-- Row 2 -->
  <div class="node">Healthcare Adapter</div>
  <div class="node">EDI Adapter</div>
  <!-- Row 3 -->
  <div class="node">Security</div>
  <div class="node">Middleware</div>
</div>
```

When service count is odd, let the last item span or leave the gap — don't force a square.

## Sizing

| Element            | Value                       |
| ------------------ | --------------------------- |
| Diagram max-width  | 1200–1600px                 |
| Body padding       | 40px 48px                   |
| Zone outer padding | 36px top, 20px sides/bottom |
| Zone gap           | 16–20px                     |
| Node min-width     | 80px                        |
| Node max-width     | 180px                       |
| Icon size          | 44×44px                     |
| Title font         | 12px bold                   |
| Desc font          | 10.5px regular              |
| Zone label font    | 12px 700 uppercase          |
| Legend font        | 12px 600                    |
