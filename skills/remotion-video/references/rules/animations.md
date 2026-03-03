# Remotion Animations

Easing curves, spring configuration, color interpolation, and timing patterns.

## Easing with interpolate

`interpolate` accepts an `easing` option from `Easing` (re-exported from React Native):

```tsx
import { interpolate, Easing } from 'remotion';

const frame = useCurrentFrame();

// Ease out — fast start, slow end (good for elements entering)
const x = interpolate(frame, [0, 30], [0, 500], {
  easing: Easing.out(Easing.cubic),
  extrapolateRight: 'clamp',
});

// Ease in — slow start, fast end (good for exits)
const opacity = interpolate(frame, [0, 20], [1, 0], {
  easing: Easing.in(Easing.quad),
  extrapolateRight: 'clamp',
});

// Ease in-out — smooth both ends
const scale = interpolate(frame, [0, 45], [0.8, 1], {
  easing: Easing.inOut(Easing.cubic),
  extrapolateRight: 'clamp',
});

// Bezier curve — full custom control
const y = interpolate(frame, [0, 60], [100, 0], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1.0),
  extrapolateRight: 'clamp',
});
```

Available Easing functions: `linear`, `quad`, `cubic`, `sin`, `circle`, `exp`, `elastic`, `back`, `bounce`, `poly(n)`, `bezier(x1, y1, x2, y2)`.

## spring() Configuration

Spring animates from 0 to 1. Config controls the feel:

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Snappy — quick settle, no bounce
const snappy = spring({ frame, fps, config: { damping: 20, stiffness: 180, mass: 1 } });

// Bouncy — overshoots and oscillates
const bouncy = spring({ frame, fps, config: { damping: 6, stiffness: 80, mass: 1 } });

// Slow and heavy
const heavy = spring({ frame, fps, config: { damping: 15, stiffness: 40, mass: 2 } });

// Default (good for most UI)
const standard = spring({ frame, fps, config: { damping: 12, stiffness: 100, mass: 1 } });
```

### Config mental model

| Goal                    | damping | stiffness | mass |
| ----------------------- | ------- | --------- | ---- |
| No bounce, fast         | 20-30   | 150-200   | 1    |
| No bounce, standard     | 12-15   | 100       | 1    |
| Slight bounce           | 8-10    | 80-100    | 1    |
| Full bounce             | 4-6     | 60-80     | 1    |
| Heavy/slow              | 12      | 40-60     | 2-3  |

### measureSpring

Calculate how many frames a spring takes to settle (useful for timing sequences):

```tsx
import { measureSpring } from 'remotion';

const frames = measureSpring({
  fps: 30,
  config: { damping: 12, stiffness: 100, mass: 1 },
  threshold: 0.01, // settle within 1% of target
});
// frames: ~28 at 30fps with default config
```

Use `measureSpring` to auto-calculate `durationInFrames` for a Sequence:

```tsx
const springDuration = measureSpring({ fps, config: springConfig, threshold: 0.005 });
```

## Delayed Animations

Start a spring after N frames using `delay`:

```tsx
const scale = spring({
  frame,
  fps,
  delay: 15,  // wait 15 frames before starting
  config: { damping: 12, stiffness: 100 },
});
```

With `interpolate`, offset the input range:

```tsx
// Start fade at frame 30
const opacity = interpolate(frame, [30, 60], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

## Staggered Entrance

Apply different delays per item using index:

```tsx
const items = ['Step 1', 'Step 2', 'Step 3'];

const StaggeredList: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div>
      {items.map((item, i) => {
        const delay = i * 8; // 8 frames between each
        const opacity = interpolate(frame, [delay, delay + 20], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const y = interpolate(frame, [delay, delay + 20], [20, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        return (
          <div key={i} style={{ opacity, transform: `translateY(${y}px)`, marginBottom: 16 }}>
            {item}
          </div>
        );
      })}
    </div>
  );
};
```

## interpolateColors

Interpolate between colors (hex, rgb, hsl):

```tsx
import { interpolateColors } from 'remotion';

const frame = useCurrentFrame();

// Single transition
const bg = interpolateColors(frame, [0, 60], ['#1a1a2e', '#16213e']);

// Multi-stop color animation
const accent = interpolateColors(
  frame,
  [0, 30, 60, 90],
  ['#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff']
);

// Use in style
return <div style={{ backgroundColor: bg, color: accent }}>Animated</div>;
```

## Exit Animations

For elements that leave the screen, invert the interpolation range:

```tsx
const { durationInFrames } = useVideoConfig();

// Fade out in last 20 frames
const opacity = interpolate(
  frame,
  [durationInFrames - 20, durationInFrames],
  [1, 0],
  { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
);
```

## Combined Enter + Exit

```tsx
const opacity = interpolate(
  frame,
  [0, 15, durationInFrames - 15, durationInFrames],
  [0, 1,  1,                     0],
  { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
);
```

## Complete Working Example

```tsx
import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  interpolateColors,
  measureSpring,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const SPRING_CONFIG = { damping: 12, stiffness: 100, mass: 1 } as const;

export const AnimationShowcase: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const springVal = spring({ frame, fps, config: SPRING_CONFIG });
  const scale = interpolate(springVal, [0, 1], [0.5, 1]);

  const slideX = interpolate(frame, [0, 30], [-200, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  const bg = interpolateColors(frame, [0, durationInFrames], ['#0f0f0f', '#1a1a2e']);

  const exitOpacity = interpolate(
    frame,
    [durationInFrames - 20, durationInFrames],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: bg, justifyContent: 'center', alignItems: 'center' }}>
      <div style={{
        transform: `scale(${scale}) translateX(${slideX}px)`,
        opacity: exitOpacity,
        fontSize: 64,
        color: '#fff',
      }}>
        Animated
      </div>
    </AbsoluteFill>
  );
};
```
