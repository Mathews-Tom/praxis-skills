# Remotion Compositions

How to define, register, and organize compositions — the top-level containers for Remotion videos.

## registerRoot and Composition

Every Remotion project has a root file that calls `registerRoot`. This is the entry point Remotion uses to discover compositions.

```tsx
// src/Root.tsx
import { Composition } from 'remotion';
import { MyVideo } from './MyVideo';

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="MyVideo"           // Unique ID used in CLI: npx remotion render MyVideo
        component={MyVideo}
        durationInFrames={150} // 5 seconds at 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

```tsx
// src/index.ts
import { registerRoot } from 'remotion';
import { Root } from './Root';

registerRoot(Root);
```

## Common Composition Sizes

| Format              | Width | Height | Aspect ratio |
| ------------------- | ----- | ------ | ------------ |
| 1080p (standard)    | 1920  | 1080   | 16:9         |
| 4K                  | 3840  | 2160   | 16:9         |
| Instagram square    | 1080  | 1080   | 1:1          |
| Instagram story     | 1080  | 1920   | 9:16         |
| Twitter/X video     | 1280  | 720    | 16:9         |
| LinkedIn video      | 1920  | 1080   | 16:9         |

## Composition Props with Zod Schema

Define and validate composition props using Zod (built into Remotion):

```tsx
import { z } from 'zod';
import { Composition } from 'remotion';

const mySchema = z.object({
  title: z.string(),
  accentColor: z.string().default('#4ade80'),
  durationSeconds: z.number().min(1).max(120).default(10),
});

type MyProps = z.infer<typeof mySchema>;

const MyVideo: React.FC<MyProps> = ({ title, accentColor, durationSeconds }) => {
  // ...
};

export const Root: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyVideo}
      schema={mySchema}
      defaultProps={{
        title: 'Default Title',
        accentColor: '#4ade80',
        durationSeconds: 10,
      }}
      durationInFrames={300}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

Props defined via schema appear as editable fields in Remotion Studio.

## calculateMetadata

Use `calculateMetadata` when the composition's duration or size depends on props:

```tsx
import { Composition, calculateMetadata } from 'remotion';
import { z } from 'zod';

const schema = z.object({
  words: z.array(z.string()),
  framesPerWord: z.number().default(30),
});

type Props = z.infer<typeof schema>;

const WordReveal: React.FC<Props> = ({ words, framesPerWord }) => {
  // render words one by one
};

const calcMeta = calculateMetadata<Props>({
  calculate: ({ props }) => ({
    durationInFrames: props.words.length * props.framesPerWord,
    fps: 30,
    width: 1920,
    height: 1080,
    props,
  }),
});

export const Root: React.FC = () => {
  return (
    <Composition
      id="WordReveal"
      component={WordReveal}
      schema={schema}
      defaultProps={{ words: ['Hello', 'World'], framesPerWord: 30 }}
      calculateMetadata={calcMeta}
    />
  );
};
```

## Folder

Group related compositions in Remotion Studio's sidebar:

```tsx
import { Composition, Folder } from 'remotion';

export const Root: React.FC = () => {
  return (
    <>
      <Folder name="Marketing">
        <Composition id="ProductLaunch" component={ProductLaunch} durationInFrames={300} fps={30} width={1920} height={1080} />
        <Composition id="SocialClip" component={SocialClip} durationInFrames={90} fps={30} width={1080} height={1080} />
      </Folder>
      <Folder name="Explainers">
        <Composition id="HowItWorks" component={HowItWorks} durationInFrames={450} fps={30} width={1920} height={1080} />
      </Folder>
    </>
  );
};
```

## Multiple Compositions for Batch Rendering

Define multiple compositions with different default props — useful for A/B variants or locale versions:

```tsx
const variants = [
  { id: 'VideoEN', lang: 'en', title: 'Hello World' },
  { id: 'VideoES', lang: 'es', title: 'Hola Mundo' },
  { id: 'VideoFR', lang: 'fr', title: 'Bonjour Monde' },
];

export const Root: React.FC = () => {
  return (
    <>
      {variants.map(({ id, lang, title }) => (
        <Composition
          key={id}
          id={id}
          component={LocalizedVideo}
          defaultProps={{ lang, title }}
          durationInFrames={150}
          fps={30}
          width={1920}
          height={1080}
        />
      ))}
    </>
  );
};
```

## Still Composition

Render a single frame (useful for thumbnails, OG images):

```tsx
import { Still } from 'remotion';

export const Root: React.FC = () => {
  return (
    <Still
      id="Thumbnail"
      component={ThumbnailComponent}
      width={1280}
      height={720}
      defaultProps={{ title: 'Video Title' }}
    />
  );
};
```

Render with: `npx remotion still Thumbnail --output thumbnail.png`

## Complete Working Example

```tsx
// src/Root.tsx
import React from 'react';
import { Composition, Folder, Still } from 'remotion';
import { z } from 'zod';
import { ExplainerVideo } from './ExplainerVideo';
import { Thumbnail } from './Thumbnail';

const explainerSchema = z.object({
  title: z.string().default('My Explainer'),
  sections: z.array(z.object({ heading: z.string(), body: z.string() })),
  accentColor: z.string().default('#6366f1'),
});

export const Root: React.FC = () => {
  return (
    <>
      <Folder name="Explainers">
        <Composition
          id="ExplainerVideo"
          component={ExplainerVideo}
          schema={explainerSchema}
          defaultProps={{
            title: 'How It Works',
            sections: [
              { heading: 'Step 1', body: 'Do the first thing.' },
              { heading: 'Step 2', body: 'Do the second thing.' },
            ],
            accentColor: '#6366f1',
          }}
          durationInFrames={450}
          fps={30}
          width={1920}
          height={1080}
        />
      </Folder>
      <Still
        id="ExplainerThumbnail"
        component={Thumbnail}
        width={1280}
        height={720}
        defaultProps={{ title: 'How It Works', accentColor: '#6366f1' }}
      />
    </>
  );
};
```
