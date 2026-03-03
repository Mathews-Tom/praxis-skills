# Remotion Subtitles and Captions

Caption system, SRT/VTT parsing, word-level timing, and styled subtitle display.

## @remotion/captions

Install the Remotion captions package:

```bash
npm install @remotion/captions
```

## Parsing SRT Files

SRT format:

```
1
00:00:01,000 --> 00:00:03,500
Hello, welcome to this video.

2
00:00:04,000 --> 00:00:07,000
Today we'll learn about Remotion.
```

Parse SRT into caption objects:

```tsx
import { parseSrt } from '@remotion/captions';

const srtContent = `1
00:00:01,000 --> 00:00:03,500
Hello, welcome to this video.

2
00:00:04,000 --> 00:00:07,000
Today we will learn about Remotion.`;

const captions = parseSrt({ input: srtContent });
// Returns: Array<{ startMs: number, endMs: number, text: string, confidence: null }>
```

## Displaying Captions

Convert milliseconds to frames using fps, then check if current frame is within each caption's range:

```tsx
import React from 'react';
import { parseSrt } from '@remotion/captions';
import { useCurrentFrame, useVideoConfig } from 'remotion';

const SRT_CONTENT = `1
00:00:00,000 --> 00:00:02,500
Hello, welcome to this video.

2
00:00:03,000 --> 00:00:06,000
Today we will learn about Remotion.`;

const captions = parseSrt({ input: SRT_CONTENT });

export const Subtitles: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = (frame / fps) * 1000;

  const activeCaption = captions.find(
    (c) => currentMs >= c.startMs && currentMs <= c.endMs
  );

  if (!activeCaption) return null;

  return (
    <div style={{
      position: 'absolute',
      bottom: 80,
      left: 0,
      right: 0,
      display: 'flex',
      justifyContent: 'center',
      padding: '0 120px',
    }}>
      <div style={{
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        color: '#ffffff',
        fontSize: 36,
        fontWeight: 500,
        padding: '12px 24px',
        borderRadius: 8,
        textAlign: 'center',
        lineHeight: 1.4,
        backdropFilter: 'blur(4px)',
      }}>
        {activeCaption.text}
      </div>
    </div>
  );
};
```

## Word-Level Timing (Karaoke Style)

Use `@remotion/captions`'s `serializeTranscript` or build word-level timing manually:

```tsx
type WordTiming = {
  word: string;
  startMs: number;
  endMs: number;
};

type KaraokeProps = {
  words: WordTiming[];
};

export const KaraokeSubtitle: React.FC<KaraokeProps> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = (frame / fps) * 1000;

  return (
    <div style={{
      position: 'absolute',
      bottom: 80,
      left: 0,
      right: 0,
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'center',
      gap: 8,
      padding: '0 120px',
    }}>
      {words.map((w, i) => {
        const isActive = currentMs >= w.startMs && currentMs <= w.endMs;
        const isPast = currentMs > w.endMs;

        return (
          <span
            key={i}
            style={{
              fontSize: 36,
              fontWeight: 600,
              color: isActive ? '#fbbf24' : isPast ? 'rgba(255,255,255,0.5)' : '#ffffff',
              transition: 'none', // no CSS transitions in Remotion
              textShadow: isActive ? '0 0 20px rgba(251, 191, 36, 0.5)' : 'none',
            }}
          >
            {w.word}
          </span>
        );
      })}
    </div>
  );
};
```

## Generating Word Timing from SRT

Split SRT captions into per-word timing by distributing time evenly:

```tsx
import { parseSrt } from '@remotion/captions';

type WordTiming = { word: string; startMs: number; endMs: number };

function srtToWordTimings(srtContent: string): WordTiming[] {
  const captions = parseSrt({ input: srtContent });
  const wordTimings: WordTiming[] = [];

  for (const caption of captions) {
    const words = caption.text.split(' ').filter(Boolean);
    const durationPerWord = (caption.endMs - caption.startMs) / words.length;

    words.forEach((word, i) => {
      wordTimings.push({
        word,
        startMs: caption.startMs + i * durationPerWord,
        endMs: caption.startMs + (i + 1) * durationPerWord,
      });
    });
  }

  return wordTimings;
}
```

## Styled Caption Variants

**Lower-third style:**

```tsx
<div style={{
  position: 'absolute', bottom: 60, left: 60, right: 60,
  backgroundColor: '#18181b',
  borderLeft: '4px solid #6366f1',
  padding: '16px 24px',
  borderRadius: '0 8px 8px 0',
  color: '#f4f4f5',
  fontSize: 32,
  fontWeight: 500,
}}>
  {activeCaption?.text}
</div>
```

**Centered, no background (white text with shadow):**

```tsx
<div style={{
  position: 'absolute', bottom: 80, left: 0, right: 0,
  textAlign: 'center',
  color: '#ffffff',
  fontSize: 40,
  fontWeight: 700,
  textShadow: '0 2px 8px rgba(0,0,0,0.8), 0 0 24px rgba(0,0,0,0.5)',
  padding: '0 100px',
}}>
  {activeCaption?.text}
</div>
```

## Complete Working Example

```tsx
import React from 'react';
import { parseSrt } from '@remotion/captions';
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';

const SRT = `1
00:00:00,500 --> 00:00:03,000
Welcome to our product demo.

2
00:00:03,500 --> 00:00:06,500
See how it works in three steps.

3
00:00:07,000 --> 00:00:10,000
Let us get started.`;

const captionData = parseSrt({ input: SRT });

const CaptionOverlay: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;

  const active = captionData.find((c) => ms >= c.startMs && ms <= c.endMs);
  if (!active) return null;

  const captionFrame = frame - Math.floor((active.startMs / 1000) * fps);
  const opacity = interpolate(captionFrame, [0, 8], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      position: 'absolute', bottom: 72, left: 0, right: 0,
      display: 'flex', justifyContent: 'center',
      opacity,
    }}>
      <div style={{
        backgroundColor: 'rgba(9,9,11,0.82)',
        color: '#fafafa',
        fontSize: 34,
        fontWeight: 500,
        padding: '10px 20px',
        borderRadius: 6,
        lineHeight: 1.5,
        maxWidth: 900,
        textAlign: 'center',
      }}>
        {active.text}
      </div>
    </div>
  );
};

type CaptionedVideoProps = {
  voiceoverFile: string;
};

export const CaptionedVideo: React.FC<CaptionedVideoProps> = ({ voiceoverFile }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#09090b' }}>
      <Audio src={staticFile(voiceoverFile)} volume={1} />
      {/* Visual content here */}
      <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
        <p style={{ color: '#71717a', fontSize: 40 }}>Video content</p>
      </AbsoluteFill>
      <CaptionOverlay />
    </AbsoluteFill>
  );
};
```
