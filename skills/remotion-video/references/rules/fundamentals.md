# Remotion Fundamentals

Core building blocks for every Remotion video. Every animation derives from frame number and video config.

## useCurrentFrame

Returns the current frame number (0-indexed). The frame number is the single source of truth for all animation state.

```tsx
import { useCurrentFrame } from 'remotion';

const MyComponent: React.FC = () => {
  const frame = useCurrentFrame(); // 0, 1, 2, ... durationInFrames - 1
  return <div>Frame: {frame}</div>;
};
```

Never use `Date.now()`, `performance.now()`, `Math.random()`, or `setTimeout` inside components — outputs must be deterministic per frame.

## useVideoConfig

Returns the composition's configuration: fps, width, height, durationInFrames.

```tsx
import { useVideoConfig } from 'remotion';

const MyComponent: React.FC = () => {
  const { fps, width, height, durationInFrames } = useVideoConfig();
  // fps: frames per second (e.g., 30)
  // width/height: canvas size in pixels (e.g., 1920x1080)
  // durationInFrames: total frames in this composition
  const totalSeconds = durationInFrames / fps;
  return <div>{totalSeconds}s video at {fps}fps</div>;
};
```

## interpolate

Maps a value from one range to another. Use for linear animations driven by frame number.

```tsx
import { interpolate } from 'remotion';

const opacity = interpolate(
  frame,           // input value
  [0, 30],         // input range: frames 0 to 30
  [0, 1],          // output range: 0 to 1
  {
    extrapolateLeft: 'clamp',   // don't go below 0 before frame 0
    extrapolateRight: 'clamp',  // don't go above 1 after frame 30
  }
);
```

Multiple keyframes work the same way:

```tsx
const x = interpolate(
  frame,
  [0, 30, 60, 90],      // 4 keyframes
  [0, 100, 100, 200],   // hold at 100 between frames 30-60, then move again
  { extrapolateRight: 'clamp' }
);
```

Always clamp extrapolation unless you intentionally want values to extend beyond the range.

## spring

Physics-based animation. Preferred over easing curves for natural motion.

```tsx
import { spring } from 'remotion';
import { useCurrentFrame, useVideoConfig } from 'remotion';

const MyComponent: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: {
      damping: 12,     // higher = less oscillation (>= 10 for no bounce)
      stiffness: 100,  // higher = faster
      mass: 1,         // higher = slower, more inertia
    },
    // Optional: delay start
    delay: 10,         // wait 10 frames before starting
    // Optional: clamp to [0, 1]
    durationRestThresholdInMs: 10,
  });

  return <div style={{ transform: `scale(${scale})` }}>Hello</div>;
};
```

Spring output is approximately 0 at frame 0 and converges to 1. Use with `interpolate` to map to any range:

```tsx
const translateX = interpolate(scale, [0, 1], [-200, 0]);
```

## Sequence

Places child content at a specific start frame with an optional duration. The child's `useCurrentFrame()` resets to 0 at the sequence's start.

```tsx
import { Sequence } from 'remotion';

const MyVideo: React.FC = () => {
  return (
    <>
      <Sequence from={0} durationInFrames={60}>
        <TitleCard />         {/* plays frames 0-59 */}
      </Sequence>
      <Sequence from={60} durationInFrames={90}>
        <ContentSection />    {/* plays frames 60-149, but its frame starts at 0 */}
      </Sequence>
      <Sequence from={150}>
        <Outro />             {/* plays from frame 150 to end */}
      </Sequence>
    </>
  );
};
```

Within `<ContentSection />`, `useCurrentFrame()` returns 0-89 (not 60-149).

## Series

Convenience wrapper that places sequences back-to-back without manual `from` calculation.

```tsx
import { Series } from 'remotion';

const MyVideo: React.FC = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={60}>
        <TitleCard />
      </Series.Sequence>
      <Series.Sequence durationInFrames={90}>
        <ContentSection />
      </Series.Sequence>
      <Series.Sequence durationInFrames={45}>
        <Outro />
      </Series.Sequence>
    </Series>
  );
};
```

## AbsoluteFill

Full-width/height positioned div. Use as the root element of every scene component.

```tsx
import { AbsoluteFill } from 'remotion';

const TitleCard: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a2e', justifyContent: 'center', alignItems: 'center' }}>
      <h1 style={{ color: 'white', fontSize: 72 }}>Title</h1>
    </AbsoluteFill>
  );
};
```

`AbsoluteFill` is equivalent to `position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex`.

## Complete Working Example

```tsx
import React from 'react';
import {
  AbsoluteFill,
  Sequence,
  Series,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const FadeInTitle: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const y = interpolate(frame, [0, 20], [30, 0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#0f0f0f' }}>
      <h1 style={{ color: '#fff', fontSize: 80, opacity, transform: `translateY(${y}px)` }}>
        {text}
      </h1>
    </AbsoluteFill>
  );
};

const BounceIn: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 120 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#0f0f0f' }}>
      <div style={{ transform: `scale(${scale})` }}>{children}</div>
    </AbsoluteFill>
  );
};

export const DemoVideo: React.FC = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={60}>
        <FadeInTitle text="Hello, Remotion" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={60}>
        <BounceIn>
          <p style={{ fontSize: 48, color: '#4ade80' }}>It works!</p>
        </BounceIn>
      </Series.Sequence>
    </Series>
  );
};
```
