# Remotion TailwindCSS Integration

Using TailwindCSS utility classes for styling in Remotion videos.

## Setup

Install TailwindCSS and the Remotion Tailwind plugin:

```bash
npm install tailwindcss @remotion/tailwind
```

Add the plugin to `remotion.config.ts`:

```ts
// remotion.config.ts
import { Config } from '@remotion/cli/config';
import { enableTailwind } from '@remotion/tailwind';

Config.overrideWebpackConfig((currentConfiguration) => {
  return enableTailwind(currentConfiguration);
});
```

Create `tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Create `src/style.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Import the CSS in your root file:

```tsx
// src/Root.tsx
import './style.css';
```

## Using Tailwind Classes

Apply Tailwind classes via the `className` prop on any HTML element inside Remotion components:

```tsx
import { AbsoluteFill } from 'remotion';

const TitleCard: React.FC = () => {
  return (
    <AbsoluteFill className="bg-zinc-950 flex items-center justify-center">
      <h1 className="text-white text-8xl font-bold tracking-tighter">
        Hello, TailwindCSS
      </h1>
    </AbsoluteFill>
  );
};
```

## Mixing Tailwind and Inline Styles

Use Tailwind for static styling and inline `style` for animated values (since Tailwind classes cannot contain frame-derived values):

```tsx
import { interpolate, useCurrentFrame } from 'remotion';

const AnimatedCard: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
  const translateY = interpolate(frame, [0, 30], [40, 0], { extrapolateRight: 'clamp' });

  return (
    <div
      className="bg-white rounded-2xl shadow-2xl p-8 max-w-lg"
      style={{ opacity, transform: `translateY(${translateY}px)` }}
    >
      <h2 className="text-2xl font-semibold text-zinc-900 mb-2">Card Title</h2>
      <p className="text-zinc-500 text-base leading-relaxed">Card body text here.</p>
    </div>
  );
};
```

## Responsive Units

Remotion renders at a fixed pixel resolution. Tailwind's responsive breakpoints are not meaningful. Use Tailwind's base utility classes directly. For values that scale with resolution, use inline styles with pixel values derived from `useVideoConfig()`:

```tsx
import { useVideoConfig } from 'remotion';

const ResponsiveTitle: React.FC = () => {
  const { width, height } = useVideoConfig();
  const fontSize = width * 0.05; // 5% of canvas width

  return (
    <h1 className="font-bold text-white tracking-tighter" style={{ fontSize }}>
      Scales with canvas
    </h1>
  );
};
```

## Animation with Tailwind Variants

Tailwind's `transition`, `duration`, and `ease` classes do not work in Remotion (CSS transitions are frame-independent; Remotion ignores them). Always animate via `interpolate` or `spring` in inline styles.

Tailwind IS useful for:
- Background colors, gradients (`bg-gradient-to-r from-violet-600 to-indigo-600`)
- Border radius (`rounded-xl`, `rounded-full`)
- Typography (`font-bold`, `tracking-tight`, `leading-snug`)
- Shadows (`shadow-lg`, `shadow-2xl`)
- Flexbox/grid layout (`flex items-center justify-between`, `grid grid-cols-3 gap-6`)
- Spacing (`p-8`, `gap-4`, `mt-6`)
- Opacity (static only: `opacity-50`; for animated use inline style)

## Gradient Backgrounds

```tsx
const GradientBg: React.FC = () => {
  return (
    <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      {/* content */}
    </div>
  );
};
```

## Card Grid Layout

```tsx
type FeatureItem = { icon: string; title: string; desc: string };

const FeatureGrid: React.FC<{ features: FeatureItem[] }> = ({ features }) => {
  const frame = useCurrentFrame();

  return (
    <div className="grid grid-cols-3 gap-6 w-full px-16">
      {features.map((f, i) => {
        const delay = i * 8;
        const opacity = interpolate(frame, [delay, delay + 20], [0, 1], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        });
        const y = interpolate(frame, [delay, delay + 20], [30, 0], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        });
        return (
          <div
            key={i}
            className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20"
            style={{ opacity, transform: `translateY(${y}px)` }}
          >
            <div className="text-4xl mb-3">{f.icon}</div>
            <h3 className="text-white font-semibold text-xl mb-2">{f.title}</h3>
            <p className="text-white/60 text-sm leading-relaxed">{f.desc}</p>
          </div>
        );
      })}
    </div>
  );
};
```

## Complete Working Example

```tsx
import React from 'react';
import { loadFont } from '@remotion/google-fonts/Inter';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

const { fontFamily } = loadFont('normal', { weights: ['400', '600', '700'], subsets: ['latin'] });

type HeroProps = {
  badge: string;
  headline: string;
  subheadline: string;
  ctaLabel: string;
};

export const HeroScene: React.FC<HeroProps> = ({ badge, headline, subheadline, ctaLabel }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const containerOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  const headlineScale = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  const ctaOpacity = interpolate(frame, [30, 50], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      className="bg-zinc-950 flex flex-col items-center justify-center gap-8 px-20"
      style={{ fontFamily, opacity: containerOpacity }}
    >
      {/* Badge */}
      <div className="bg-indigo-500/20 text-indigo-300 text-sm font-medium px-4 py-1.5 rounded-full border border-indigo-500/30">
        {badge}
      </div>

      {/* Headline */}
      <h1
        className="text-white text-center font-bold tracking-tighter leading-none"
        style={{ fontSize: 96, transform: `scale(${headlineScale})` }}
      >
        {headline}
      </h1>

      {/* Subheadline */}
      <p className="text-zinc-400 text-3xl text-center max-w-3xl leading-snug">
        {subheadline}
      </p>

      {/* CTA */}
      <button
        className="bg-white text-zinc-900 font-semibold text-2xl px-10 py-4 rounded-2xl"
        style={{ opacity: ctaOpacity, border: 'none', cursor: 'default' }}
      >
        {ctaLabel}
      </button>
    </AbsoluteFill>
  );
};
```
