# Remotion Text and Fonts

Loading web fonts, local fonts, text measurement, and typography patterns.

## @remotion/google-fonts

The recommended way to load Google Fonts. Fonts are fetched at bundle time and included in the render.

Install: `npm install @remotion/google-fonts`

```tsx
// Load a font — do this at the module level, outside any component
import { loadFont } from '@remotion/google-fonts/Inter';

const { fontFamily } = loadFont('normal', {
  weights: ['400', '700'],
  subsets: ['latin'],
});

const TitleComponent: React.FC = () => {
  return (
    <div style={{ fontFamily, fontSize: 72, fontWeight: 700 }}>
      Loaded with Inter
    </div>
  );
};
```

Available packages follow the pattern `@remotion/google-fonts/<FontName>` in PascalCase without spaces:
- `@remotion/google-fonts/Inter`
- `@remotion/google-fonts/Roboto`
- `@remotion/google-fonts/Montserrat`
- `@remotion/google-fonts/PlusJakartaSans`
- `@remotion/google-fonts/SpaceGrotesk`
- `@remotion/google-fonts/DMMono`

Call `loadFont()` once at module level. Multiple calls with the same config are deduplicated.

## Multiple Weights and Styles

```tsx
import { loadFont } from '@remotion/google-fonts/Inter';

// Load regular and bold, for latin subset
const { fontFamily: interRegular } = loadFont('normal', {
  weights: ['400'],
  subsets: ['latin'],
});

const { fontFamily: interBold } = loadFont('normal', {
  weights: ['700'],
  subsets: ['latin'],
});

// fontFamily value is the same — CSS fontWeight controls the weight
```

## Local Fonts with @remotion/fonts

For custom brand fonts not on Google Fonts:

```tsx
import { loadFont } from '@remotion/fonts';
import { staticFile } from 'remotion';

// Call once at module level
loadFont({
  family: 'BrandFont',
  url: staticFile('fonts/BrandFont-Regular.woff2'),
  weight: '400',
});

loadFont({
  family: 'BrandFont',
  url: staticFile('fonts/BrandFont-Bold.woff2'),
  weight: '700',
});

const BrandText: React.FC = () => {
  return (
    <div style={{ fontFamily: 'BrandFont', fontWeight: 700, fontSize: 64 }}>
      Brand Headline
    </div>
  );
};
```

Place font files in `public/fonts/`.

## delayRender for Font Loading

If fonts are loaded dynamically (not via `@remotion/google-fonts`), pause rendering until they're ready:

```tsx
import { delayRender, continueRender } from 'remotion';
import { useEffect, useState } from 'react';

const FontLoader: React.FC = () => {
  const [loaded, setLoaded] = useState(false);
  const [handle] = useState(() => delayRender('Loading custom font'));

  useEffect(() => {
    const font = new FontFace('MyFont', 'url(/fonts/MyFont.woff2)');
    font.load().then((loaded) => {
      document.fonts.add(loaded);
      setLoaded(true);
      continueRender(handle);
    });
  }, [handle]);

  if (!loaded) return null;

  return <div style={{ fontFamily: 'MyFont' }}>Ready</div>;
};
```

With `@remotion/google-fonts` and `@remotion/fonts`, this is handled automatically — no manual `delayRender` needed.

## Typography Best Practices

```tsx
// Title — dominant, minimal
<h1 style={{
  fontFamily,
  fontSize: 80,
  fontWeight: 700,
  letterSpacing: '-0.02em',
  lineHeight: 1.1,
  color: '#ffffff',
  margin: 0,
}}>Main Title</h1>

// Subheading — clear hierarchy
<h2 style={{
  fontFamily,
  fontSize: 40,
  fontWeight: 500,
  letterSpacing: '-0.01em',
  color: '#a1a1aa',
  margin: 0,
}}>Subtitle</h2>

// Body — readable at distance
<p style={{
  fontFamily,
  fontSize: 28,
  fontWeight: 400,
  lineHeight: 1.6,
  color: '#e4e4e7',
  maxWidth: 800,
}}>Body text here.</p>

// Code / monospace
<code style={{
  fontFamily: '"DM Mono", monospace',
  fontSize: 24,
  backgroundColor: '#1e1e2e',
  padding: '4px 8px',
  borderRadius: 4,
  color: '#cdd6f4',
}}>const x = 42</code>
```

## Animated Text — Character by Character

Reveal text letter by letter using frame-based timing:

```tsx
import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

type TypewriterProps = {
  text: string;
  framesPerChar?: number;
  fontFamily: string;
};

export const Typewriter: React.FC<TypewriterProps> = ({ text, framesPerChar = 2, fontFamily }) => {
  const frame = useCurrentFrame();
  const charsToShow = Math.floor(frame / framesPerChar);
  const visible = text.slice(0, charsToShow);
  const cursor = charsToShow < text.length ? '|' : '';

  return (
    <div style={{ fontFamily, fontSize: 48, color: '#fff', letterSpacing: '0.02em' }}>
      {visible}{cursor}
    </div>
  );
};
```

## Word-by-Word Reveal

```tsx
type WordRevealProps = {
  words: string[];
  framesPerWord?: number;
  fontFamily: string;
};

export const WordReveal: React.FC<WordRevealProps> = ({ words, framesPerWord = 15, fontFamily }) => {
  const frame = useCurrentFrame();

  return (
    <div style={{ fontFamily, fontSize: 56, color: '#fff', display: 'flex', gap: 16, flexWrap: 'wrap' }}>
      {words.map((word, i) => {
        const startFrame = i * framesPerWord;
        const opacity = interpolate(frame, [startFrame, startFrame + 10], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const y = interpolate(frame, [startFrame, startFrame + 10], [20, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        return (
          <span key={i} style={{ opacity, display: 'inline-block', transform: `translateY(${y}px)` }}>
            {word}
          </span>
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
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

const { fontFamily } = loadFont('normal', { weights: ['400', '600', '700'], subsets: ['latin'] });

type TitleCardProps = {
  headline: string;
  subheadline: string;
};

export const TitleCard: React.FC<TitleCardProps> = ({ headline, subheadline }) => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [0, 20], [30, 0], { extrapolateRight: 'clamp' });

  const subOpacity = interpolate(frame, [15, 35], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const subY = interpolate(frame, [15, 35], [20, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#09090b',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
      gap: 16,
      padding: 80,
    }}>
      <h1 style={{
        fontFamily,
        fontSize: 88,
        fontWeight: 700,
        color: '#fafafa',
        margin: 0,
        textAlign: 'center',
        letterSpacing: '-0.03em',
        opacity: titleOpacity,
        transform: `translateY(${titleY}px)`,
      }}>
        {headline}
      </h1>
      <p style={{
        fontFamily,
        fontSize: 36,
        fontWeight: 400,
        color: '#71717a',
        margin: 0,
        textAlign: 'center',
        opacity: subOpacity,
        transform: `translateY(${subY}px)`,
      }}>
        {subheadline}
      </p>
    </AbsoluteFill>
  );
};
```
