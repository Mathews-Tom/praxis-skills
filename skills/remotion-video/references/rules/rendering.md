# Remotion Rendering

CLI render commands, renderMedia API, quality presets, and format options.

## CLI Render

The standard way to render a composition to a file:

```bash
npx remotion render <CompositionId> [output]
```

Basic example:

```bash
npx remotion render MyVideo out/video.mp4
```

Render a specific composition in a multi-composition project:

```bash
npx remotion render --composition=ProductLaunch out/product.mp4
```

## Quality / Resolution Flags

Control output resolution and FPS:

```bash
# 1080p, 30fps (default for most projects)
npx remotion render MyVideo out/video.mp4

# 720p output via scale
npx remotion render MyVideo out/preview.mp4 --scale=0.667

# 4K — set composition width/height to 3840x2160 in Root.tsx
npx remotion render MyVideo out/4k.mp4
```

## Frame Rate

The FPS is defined in the `<Composition>` component. To render at a different FPS, modify the composition's `fps` prop. You cannot override FPS at render time — it is baked into the composition.

## Format Options

```bash
# H.264 MP4 (default, broadest compatibility)
npx remotion render MyVideo out/video.mp4

# WebM (VP8/VP9, web-optimized)
npx remotion render MyVideo out/video.webm

# GIF (keep short, max 10s for reasonable file size)
npx remotion render MyVideo out/animation.gif --scale=0.5

# PNG sequence (one image per frame)
npx remotion render MyVideo out/frames/ --sequence
```

## Codec Selection

```bash
# H.264 (default for mp4)
npx remotion render MyVideo out/video.mp4 --codec=h264

# H.265/HEVC (better compression, less compatible)
npx remotion render MyVideo out/video.mp4 --codec=h265

# VP8 for WebM
npx remotion render MyVideo out/video.webm --codec=vp8

# VP9 for WebM (better quality)
npx remotion render MyVideo out/video.webm --codec=vp9
```

## Concurrency

Control how many browser tabs render frames in parallel. Higher = faster but more RAM:

```bash
# Default: uses half of CPU cores
npx remotion render MyVideo out/video.mp4

# Explicit concurrency (reduce if running out of memory)
npx remotion render MyVideo out/video.mp4 --concurrency=4

# Maximum speed (may run out of RAM on long videos)
npx remotion render MyVideo out/video.mp4 --concurrency=16
```

## Partial Render (Frame Range)

Render only a subset of frames — useful for testing a section:

```bash
# Render frames 0-89 (first 3 seconds at 30fps)
npx remotion render MyVideo out/preview.mp4 --frames=0-89

# Render a single frame as PNG
npx remotion still MyVideo out/frame.png --frame=30
```

## Passing Props via CLI

Override composition props at render time:

```bash
npx remotion render MyVideo out/video.mp4 --props='{"title":"Custom Title","accentColor":"#ff6b6b"}'
```

Or pass a JSON file:

```bash
npx remotion render MyVideo out/video.mp4 --props=./props.json
```

## renderMedia API (Programmatic)

Use the Node.js API to render from scripts — required for batch generation.

Install the renderer:

```bash
npm install @remotion/renderer
```

Basic usage:

```ts
import { renderMedia, selectComposition } from '@remotion/renderer';
import path from 'path';

const bundleLocation = await bundle({
  entryPoint: path.join(process.cwd(), 'src/index.ts'),
});

const composition = await selectComposition({
  serveUrl: bundleLocation,
  id: 'MyVideo',
  inputProps: { title: 'Hello World' },
});

await renderMedia({
  composition,
  serveUrl: bundleLocation,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
  inputProps: { title: 'Hello World' },
  onProgress: ({ progress }) => {
    process.stdout.write(`\rRendering: ${Math.round(progress * 100)}%`);
  },
});
```

## bundle API

Bundle the project before rendering programmatically:

```ts
import { bundle } from '@remotion/bundler';
import path from 'path';
import { enableTailwind } from '@remotion/tailwind';

const bundleLocation = await bundle({
  entryPoint: path.join(process.cwd(), 'src/index.ts'),
  // Apply same webpack overrides as remotion.config.ts
  webpackOverride: enableTailwind,
});
```

## Still Rendering (Single Frame)

Render a single frame to PNG/JPEG — useful for thumbnails and OG images:

```bash
# CLI
npx remotion still Thumbnail out/thumbnail.png --frame=0

# Props override
npx remotion still Thumbnail out/thumb-custom.png --props='{"title":"Custom"}'
```

Programmatic:

```ts
import { renderStill } from '@remotion/renderer';

await renderStill({
  composition,
  serveUrl: bundleLocation,
  output: 'out/thumbnail.png',
  imageFormat: 'png',
  inputProps: { title: 'Custom Thumbnail' },
});
```

## Quality Presets (scripts/render.sh reference)

| Preset    | Resolution | FPS | Concurrency | Use case               |
| --------- | ---------- | --- | ----------- | ---------------------- |
| `preview` | 480p (0.25x scale) | composition fps | 2 | Fast layout check |
| `draft`   | 720p (0.667x scale) | composition fps | 4 | Client draft review |
| `final`   | 1080p (1x) | composition fps | 8 | Standard delivery |
| `4k`      | 2160p (2x scale) | composition fps | 4 | Presentation quality |

Note: "scale" here means `--scale` flag passed to `npx remotion render`. The composition's width/height defines the native resolution; `--scale` multiplies it.

## Common Render Errors

| Error                          | Cause                                      | Resolution                                            |
| ------------------------------ | ------------------------------------------ | ----------------------------------------------------- |
| `Composition not found`        | Wrong ID in CLI command                    | Check `<Composition id=` matches command              |
| `ENOMEM` / heap out of memory  | Too many concurrent frames in RAM          | Reduce `--concurrency`                                |
| `delayRender timed out`        | Async fetch > 30s                          | Increase `timeoutInMilliseconds` in `delayRender`     |
| `ERR_MODULE_NOT_FOUND`         | Missing npm package                        | Run `npm install`                                     |
| Corrupted output               | Interrupted render                         | Delete partial output, re-render                      |
| No audio in output             | ffmpeg not found                           | Install ffmpeg: `brew install ffmpeg`                 |
