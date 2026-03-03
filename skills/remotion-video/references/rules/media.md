# Remotion Media

Loading and displaying images, video, and audio assets in Remotion.

## staticFile

Resolves a file from the `public/` directory to a URL usable in Remotion components. Always use `staticFile` — never hardcode paths.

```tsx
import { staticFile } from 'remotion';

const logoUrl = staticFile('logo.png');       // → /public/logo.png resolved correctly
const videoUrl = staticFile('hero.mp4');
const audioUrl = staticFile('music.mp3');
```

Place all assets in the `public/` folder at the project root.

## Img

Use `<Img>` instead of `<img>` for images. Remotion's `<Img>` pauses rendering until the image loads, ensuring it appears on the correct frame.

```tsx
import { Img, staticFile } from 'remotion';

const LogoScene: React.FC = () => {
  return (
    <Img
      src={staticFile('logo.png')}
      style={{
        width: 200,
        height: 'auto',
        objectFit: 'contain',
      }}
    />
  );
};
```

For remote images (URLs), `<Img>` works the same way — it blocks rendering until the image loads.

## Video (inline video)

Embeds a video asset that plays in sync with the Remotion timeline. The video's playback position is driven by the current frame.

```tsx
import { Video, staticFile, useVideoConfig } from 'remotion';

const VideoEmbed: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <Video
      src={staticFile('clip.mp4')}
      startFrom={0}          // start from this frame of the source video
      endAt={90}             // stop at this frame of the source video
      playbackRate={1}       // 1 = normal speed, 2 = 2x
      volume={0.8}           // 0 to 1
      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
    />
  );
};
```

`<Video>` renders frames in-process. For best render quality and accuracy, prefer `<OffthreadVideo>` in final renders.

## OffthreadVideo

Renders video frames in a separate thread. More accurate for complex video sources (e.g., H.264 with B-frames). Required for videos that don't decode correctly with `<Video>`.

```tsx
import { OffthreadVideo, staticFile } from 'remotion';

const BackgroundVideo: React.FC = () => {
  return (
    <OffthreadVideo
      src={staticFile('background.mp4')}
      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      muted
    />
  );
};
```

`<OffthreadVideo>` does not support `startFrom`/`endAt`. Use a `<Sequence>` with a matching offset instead:

```tsx
// Skip first 30 frames of the video by offsetting the sequence
<Sequence from={-30}>
  <OffthreadVideo src={staticFile('clip.mp4')} />
</Sequence>
```

## Audio

Plays an audio file in sync with the timeline. See `audio.md` for volume curves and trimming.

```tsx
import { Audio, staticFile } from 'remotion';

const WithMusic: React.FC = () => {
  return (
    <>
      <Audio
        src={staticFile('music.mp3')}
        volume={0.6}
        startFrom={0}
        endAt={150}
      />
      {/* visual content here */}
    </>
  );
};
```

## delayRender and continueRender

Use these to pause rendering while async assets load (e.g., fetching data from an API, loading web fonts manually).

```tsx
import { delayRender, continueRender, useEffect, useState } from 'react';
import { useCallback } from 'react';

const handle = delayRender('Loading data from API');

// Inside a component:
const DataDrivenScene: React.FC = () => {
  const [data, setData] = useState<null | SomeData>(null);

  const handleRef = useCallback(() => delayRender('Fetching chart data'), []);
  const [renderHandle] = useState(() => delayRender('Loading data'));

  useEffect(() => {
    fetch('https://api.example.com/data')
      .then(res => res.json())
      .then(json => {
        setData(json);
        continueRender(renderHandle);
      })
      .catch(err => {
        console.error(err);
        continueRender(renderHandle); // must always call, even on error
      });
  }, [renderHandle]);

  if (!data) return null;

  return <div>{JSON.stringify(data)}</div>;
};
```

`delayRender` returns a handle. Always call `continueRender(handle)` — even on errors — or rendering will hang and eventually timeout (30s default).

Increase timeout for slow resources:

```tsx
const handle = delayRender('Loading large asset', {
  timeoutInMilliseconds: 60_000, // 60 seconds
});
```

## Complete Working Example

```tsx
import React, { useEffect, useState } from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  continueRender,
  delayRender,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { interpolate } from 'remotion';

type MediaSceneProps = {
  logoFile: string;
  videoFile: string;
  audioFile: string;
};

export const MediaScene: React.FC<MediaSceneProps> = ({ logoFile, videoFile, audioFile }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const logoOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const audioVolume = interpolate(
    frame,
    [0, 15, durationInFrames - 15, durationInFrames],
    [0, 0.7, 0.7, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill>
      {/* Background video */}
      <AbsoluteFill>
        <OffthreadVideo
          src={staticFile(videoFile)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          muted
        />
      </AbsoluteFill>

      {/* Audio track with fade in/out */}
      <Audio src={staticFile(audioFile)} volume={audioVolume} />

      {/* Logo overlay */}
      <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'flex-start', padding: 40 }}>
        <Img
          src={staticFile(logoFile)}
          style={{ width: 120, opacity: logoOpacity }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```
