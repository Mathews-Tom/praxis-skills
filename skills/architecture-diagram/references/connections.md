# Connection Engine

## Schema

```javascript
{
  from: 'node-id',           // data-node-id of source
  to: 'node-id',             // data-node-id of target
  type: 'realtime',          // CSS class + marker selector (see type table)
  direction: 'forward',      // forward | backward | bidi
  label: '',                 // optional midpoint label
  route: '',                 // omit for auto-orthogonal | 'straight' for direct line
  fromSide: 'right',         // left | right | top | bottom (auto-detected if omitted)
  toSide: 'left'             // left | right | top | bottom (auto-detected if omitted)
}
```

## Connection types

| type       | CSS class       | Stroke color | Style  | Marker id   | Semantic use                         |
| ---------- | --------------- | ------------ | ------ | ----------- | ------------------------------------ |
| `realtime` | `conn-realtime` | `#0077b6`    | solid  | `ah-blue`   | REST, SOAP, API, sync requests       |
| `batch`    | `conn-batch`    | `#c74634`    | dashed | `ah-red`    | SFTP, file transfer, EDI, batch jobs |
| `event`    | `conn-event`    | `#2e7d32`    | solid  | `ah-green`  | Event-driven, pub-sub, webhooks      |
| `control`  | `conn-control`  | `#c67a2e`    | dashed | `ah-orange` | Control plane, management, config    |
| `dashed`   | `conn-dashed`   | `#6a6a6a`    | dashed | `ah-gray`   | Generic secondary                    |
| `default`  | `conn-default`  | `#0077b6`    | solid  | `ah-blue`   | Generic primary                      |

## Endpoint clearance

All connection endpoints are offset outward from the node bounding box by `CONN_MARGIN` (default 16px). This prevents lines from touching or overlapping node icons. The margin is applied in `sidePoint()` — e.g., a `right` exit point is computed as `rect.x + rect.w + 16`, not at the box edge.

Adjust `CONN_MARGIN` if icon sizes change or if denser layouts require tighter clearance (minimum 10px recommended).

## Routing algorithm

Default routing is **orthogonal** (axis-aligned segments with right-angle turns only):

1. If `route === 'straight'`: direct line between endpoints
2. If `|Δy| < 4px` OR `|Δx| < 80px`: **straight line** — collapses to direct path for near-horizontal connections and short-gap adjacent nodes (same grid row with narrow inter-column gap)
3. Otherwise: **H-V-H elbow** — horizontal from source to midpoint X, vertical to target Y, horizontal to target

The midpoint X for vertical segments = `(p1.x + p2.x) / 2 + laneOffset`.

## Lane allocation (anti-overlap)

The renderer groups connections into **corridors** — horizontal bands sharing the same gap between columns. Connections whose midpoint X falls in the same 150px quantization bucket share a corridor.

Within each corridor, connections are sorted by target Y (ascending) and assigned evenly-spaced lane offsets (14px spacing). This distributes vertical segments so they don't overlap:

```text
Corridor with 3 connections (spacing=14px, total width=28px):
  Connection to topmost target:    midX - 14px
  Connection to middle target:     midX
  Connection to bottommost target: midX + 14px
```

Sorting by target Y minimizes crossing: the connection to the topmost target gets the leftmost vertical lane, so lines don't intersect within a corridor.

## Side forcing

For three-column flow layouts (Source → Platform → Target), **always force sides**:

```javascript
{ from: 'src', to: 'platform-node', fromSide: 'right', toSide: 'left' }
{ from: 'platform-node', to: 'target', fromSide: 'right', toSide: 'left' }
```

This ensures all connections flow left-to-right with clean horizontal exit/entry.

For internal platform connections (side-by-side nodes at similar Y), force `fromSide: 'right'`, `toSide: 'left'` to get clean horizontal lines.

For vertical connections within a column, use `fromSide: 'bottom'`, `toSide: 'top'`.

Auto-detection (omitting fromSide/toSide) chooses the closest side by center-to-center vector. Reliable for simple layouts but unreliable when connections cross nested zone boundaries — prefer explicit side forcing.

## Legend

Render above the diagram. Include one entry per connection type present in the diagram:

```html
<div class="legend">
  <div class="legend-item">
    <div class="legend-line" style="color:#0077b6;"></div>
    Real-time / API
  </div>
  <div class="legend-item">
    <div class="legend-line dashed" style="color:#c74634;"></div>
    Batch / SFTP / EDI
  </div>
  <div class="legend-item">
    <div class="legend-line" style="color:#2e7d32;"></div>
    Event-Driven
  </div>
</div>
```

Add `dashed` class to `.legend-line` for dashed-stroke types (batch, control, dashed). Omit the legend entirely when all connections use `default` type.
