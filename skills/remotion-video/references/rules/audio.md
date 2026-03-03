# Remotion Audio

Audio component usage, volume curves, trimming, sound effects, and frame-synced audio.

## Audio Component

Play an audio file synchronized to the Remotion timeline:

```tsx
import { Audio, staticFile } from 'remotion';

const WithAudio: React.FC = () => {
  return (
    <>
      <Audio src={staticFile('music.mp3')} />
      {/* visual components here */}
    </>
  );
};
```

The audio plays from its beginning when the composition starts. Use `startFrom` and `endAt` to trim.

## Trimming Audio

`startFrom` and `endAt` are in frames (not seconds). Convert using fps:

```tsx
import { Audio, staticFile, useVideoConfig } from 'remotion';

const TrimmedAudio: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <Audio
      src={staticFile('music.mp3')}
      startFrom={fps * 5}   // skip first 5 seconds of the audio file
      endAt={fps * 45}      // stop at 45 seconds into the audio file
    />
  );
};
```

## Volume Control

Set a static volume (0 to 1):

```tsx
<Audio src={staticFile('music.mp3')} volume={0.6} />
```

## Volume Curves

Use a callback function for frame-by-frame volume control. The function receives the current frame and returns a volume value 0-1:

```tsx
import { Audio, staticFile, useVideoConfig } from 'remotion';
import { interpolate } from 'remotion';

const FadingAudio: React.FC = () => {
  const { durationInFrames, fps } = useVideoConfig();

  return (
    <Audio
      src={staticFile('music.mp3')}
      volume={(frame) =>
        interpolate(
          frame,
          [0, fps * 1, durationInFrames - fps * 1, durationInFrames],
          [0, 0.8, 0.8, 0],
          { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
        )
      }
    />
  );
};
```

This creates a 1-second fade-in and 1-second fade-out.

## Delayed Audio Start

Use `<Sequence>` to start audio at a specific point in the video:

```tsx
import { Audio, Sequence, staticFile } from 'remotion';

const DelayedAudio: React.FC = () => {
  return (
    <>
      {/* Music starts at frame 30 (1 second at 30fps) */}
      <Sequence from={30}>
        <Audio src={staticFile('music.mp3')} volume={0.7} />
      </Sequence>
    </>
  );
};
```

## Sound Effects

Trigger short sound effects at specific frames using `<Sequence>`:

```tsx
import { Audio, Sequence, Series, staticFile } from 'remotion';

const WithSoundEffects: React.FC = () => {
  return (
    <>
      {/* Ding at frame 30 */}
      <Sequence from={30} durationInFrames={30}>
        <Audio src={staticFile('sfx/ding.wav')} volume={1} />
      </Sequence>

      {/* Whoosh at frame 90 */}
      <Sequence from={90} durationInFrames={20}>
        <Audio src={staticFile('sfx/whoosh.wav')} volume={0.8} />
      </Sequence>

      {/* visual content */}
      <Series>
        <Series.Sequence durationInFrames={60}><SceneA /></Series.Sequence>
        <Series.Sequence durationInFrames={60}><SceneB /></Series.Sequence>
      </Series>
    </>
  );
};
```

## Multiple Audio Layers

Remotion supports multiple simultaneous `<Audio>` components. Use for music + voiceover:

```tsx
const FullAudio: React.FC = () => {
  const { durationInFrames } = useVideoConfig();

  return (
    <>
      {/* Background music, low volume */}
      <Audio
        src={staticFile('music/ambient.mp3')}
        volume={(frame) =>
          interpolate(frame, [0, 15, durationInFrames - 15, durationInFrames], [0, 0.3, 0.3, 0], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          })
        }
      />
      {/* Voiceover, full volume */}
      <Sequence from={15}>
        <Audio src={staticFile('voiceover/narration.mp3')} volume={1} />
      </Sequence>
    </>
  );
};
```

## Beat-Synced Animation

Use frame math to trigger animations on music beats:

```tsx
import { useCurrentFrame } from 'remotion';
import { interpolate } from 'remotion';

const BPM = 120;
const FPS = 30;
const FRAMES_PER_BEAT = (60 / BPM) * FPS; // = 15 frames per beat

const BeatPulse: React.FC = () => {
  const frame = useCurrentFrame();

  // Progress within current beat (0 to 1, repeating)
  const beatProgress = (frame % FRAMES_PER_BEAT) / FRAMES_PER_BEAT;

  // Pulse scale on the downbeat
  const scale = interpolate(beatProgress, [0, 0.1, 1], [1.05, 1.2, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ transform: `scale(${scale})`, width: 100, height: 100, backgroundColor: '#6366f1', borderRadius: '50%' }} />
  );
};
```

## Complete Working Example

```tsx
import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  Series,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

type AudioVideoProps = {
  musicFile: string;
  voiceoverFile: string;
};

export const AudioVideo: React.FC<AudioVideoProps> = ({ musicFile, voiceoverFile }) => {
  const { durationInFrames, fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#09090b' }}>
      {/* Ambient music: fade in 0.5s, fade out 0.5s */}
      <Audio
        src={staticFile(musicFile)}
        volume={(f) =>
          interpolate(
            f,
            [0, fps * 0.5, durationInFrames - fps * 0.5, durationInFrames],
            [0, 0.25, 0.25, 0],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
          )
        }
      />

      {/* Voiceover starts 1 second in */}
      <Sequence from={fps}>
        <Audio src={staticFile(voiceoverFile)} volume={1} />
      </Sequence>

      {/* Visual content */}
      <Series>
        <Series.Sequence durationInFrames={fps * 3}>
          <TitleSlide />
        </Series.Sequence>
        <Series.Sequence durationInFrames={fps * 5}>
          <ContentSlide />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};

const TitleSlide: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill className="flex items-center justify-center" style={{ opacity }}>
      <h1 style={{ color: '#fff', fontSize: 72 }}>Title</h1>
    </AbsoluteFill>
  );
};

const ContentSlide: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill className="flex items-center justify-center" style={{ opacity }}>
      <p style={{ color: '#a1a1aa', fontSize: 40 }}>Content here</p>
    </AbsoluteFill>
  );
};
```
