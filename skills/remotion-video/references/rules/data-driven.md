# Remotion Data-Driven Video

Dataset rendering, batch generation, parametric compositions, and selectComposition + renderMedia loops.

## The Pattern

Data-driven video = one composition + many input prop sets → many rendered files.

```text
[dataset.json] → [render loop] → [video_001.mp4, video_002.mp4, ..., video_N.mp4]
```

Every variable (name, score, color, text) is a prop. Never hardcode content in components.

## Props-First Component Design

```tsx
// BAD: hardcoded content
const UserCard: React.FC = () => {
  return <div>John Smith — Score: 94</div>;
};

// GOOD: all content via props
type UserCardProps = {
  name: string;
  score: number;
  tier: "bronze" | "silver" | "gold";
  accentColor: string;
};

const UserCard: React.FC<UserCardProps> = ({
  name,
  score,
  tier,
  accentColor,
}) => {
  return (
    <div>
      {name} — Score: {score} — {tier}
    </div>
  );
};
```

## calculateMetadata for Dynamic Duration

When duration depends on data (e.g., one slide per item):

```tsx
import { Composition, calculateMetadata } from "remotion";
import { z } from "zod";

const schema = z.object({
  items: z.array(z.object({ title: z.string(), body: z.string() })),
  framesPerSlide: z.number().default(90),
});

type Props = z.infer<typeof schema>;

const calcMeta = calculateMetadata<Props>({
  calculate: ({ props }) => ({
    durationInFrames: props.items.length * props.framesPerSlide,
    fps: 30,
    width: 1920,
    height: 1080,
    props,
  }),
});
```

## Batch Render Script (Node.js)

Render multiple videos from a dataset using `renderMedia`:

```ts
// scripts/batch-render.ts
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import { enableTailwind } from "@remotion/tailwind";
import path from "path";
import fs from "fs";

type UserRecord = {
  id: string;
  name: string;
  score: number;
  tier: "bronze" | "silver" | "gold";
};

const DATASET: UserRecord[] = JSON.parse(
  fs.readFileSync("./data/users.json", "utf-8"),
);

async function main() {
  console.log(`Bundling project...`);
  const bundleLocation = await bundle({
    entryPoint: path.join(process.cwd(), "src/index.ts"),
    webpackOverride: enableTailwind,
  });

  fs.mkdirSync("./out/batch", { recursive: true });

  for (const [i, record] of DATASET.entries()) {
    const inputProps = {
      name: record.name,
      score: record.score,
      tier: record.tier,
      accentColor:
        record.tier === "gold"
          ? "#f59e0b"
          : record.tier === "silver"
            ? "#94a3b8"
            : "#a16207",
    };

    const composition = await selectComposition({
      serveUrl: bundleLocation,
      id: "UserCard",
      inputProps,
    });

    const outputPath = `./out/batch/${record.id}.mp4`;
    console.log(
      `[${i + 1}/${DATASET.length}] Rendering ${record.name} → ${outputPath}`,
    );

    await renderMedia({
      composition,
      serveUrl: bundleLocation,
      codec: "h264",
      outputLocation: outputPath,
      inputProps,
      concurrency: 4,
      onProgress: ({ progress }) => {
        process.stdout.write(`\r  Progress: ${Math.round(progress * 100)}%`);
      },
    });

    console.log(`\n  Done: ${outputPath}`);
  }

  console.log(`\nBatch complete. ${DATASET.length} videos rendered.`);
}

main().catch(console.error);
```

Run with: `npx ts-node scripts/batch-render.ts`

## Parametric Composition

One composition that adapts to any content type via a union prop:

```tsx
type SlideContent =
  | { type: "title"; headline: string; subheadline: string }
  | { type: "stat"; label: string; value: number; unit: string }
  | { type: "quote"; text: string; author: string };

type PresentationProps = {
  slides: SlideContent[];
  brandColor: string;
  logoFile: string;
};

const SlideRenderer: React.FC<{ slide: SlideContent; brandColor: string }> = ({
  slide,
  brandColor,
}) => {
  if (slide.type === "title") {
    return (
      <div style={{ textAlign: "center" }}>
        <h1 style={{ fontSize: 72, color: "#fff" }}>{slide.headline}</h1>
        <p style={{ fontSize: 36, color: "#a1a1aa" }}>{slide.subheadline}</p>
      </div>
    );
  }
  if (slide.type === "stat") {
    return (
      <div style={{ textAlign: "center" }}>
        <span style={{ fontSize: 120, fontWeight: 700, color: brandColor }}>
          {slide.value}
        </span>
        <span style={{ fontSize: 40, color: "#fff" }}>{slide.unit}</span>
        <p style={{ fontSize: 32, color: "#a1a1aa" }}>{slide.label}</p>
      </div>
    );
  }
  return (
    <div style={{ maxWidth: 900, textAlign: "center" }}>
      <p
        style={{
          fontSize: 48,
          color: "#fff",
          fontStyle: "italic",
          lineHeight: 1.5,
        }}
      >
        "{slide.text}"
      </p>
      <p style={{ fontSize: 28, color: brandColor }}>— {slide.author}</p>
    </div>
  );
};
```

## Dataset as JSON in public/

Place datasets in `public/data/` and fetch via `delayRender`:

```tsx
import { delayRender, continueRender, staticFile } from "remotion";
import { useState, useEffect } from "react";

type DataRecord = { label: string; value: number };

export const DataFetching: React.FC = () => {
  const [data, setData] = useState<DataRecord[] | null>(null);
  const [handle] = useState(() => delayRender("Fetching chart data"));

  useEffect(() => {
    fetch(staticFile("data/chart-data.json"))
      .then((r) => r.json())
      .then((json) => {
        setData(json);
        continueRender(handle);
      })
      .catch((err) => {
        console.error("Failed to load data", err);
        continueRender(handle);
      });
  }, [handle]);

  if (!data) return null;

  return <BarChart data={data} title="Metrics" />;
};
```

## A/B Variant Rendering

Render two variants of the same composition with different props:

```ts
const variants = [
  {
    id: "video-variant-a",
    props: { headline: "Save Time", accentColor: "#6366f1" },
  },
  {
    id: "video-variant-b",
    props: { headline: "Boost Revenue", accentColor: "#f59e0b" },
  },
];

for (const variant of variants) {
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: "MarketingVideo",
    inputProps: variant.props,
  });

  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: "h264",
    outputLocation: `out/${variant.id}.mp4`,
    inputProps: variant.props,
  });
}
```

## Complete Working Example

```tsx
// src/compositions/PersonalizedCard.tsx
import React from "react";
import { loadFont } from "@remotion/google-fonts/Inter";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "700"],
  subsets: ["latin"],
});

export type PersonalizedCardProps = {
  recipientName: string;
  metric: string;
  value: number;
  unit: string;
  accentColor: string;
  badgeLabel: string;
};

export const PersonalizedCard: React.FC<PersonalizedCardProps> = ({
  recipientName,
  metric,
  value,
  unit,
  accentColor,
  badgeLabel,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const containerOpacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });
  const nameScale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
  });
  const valueProgress = spring({
    frame: Math.max(0, frame - 20),
    fps,
    config: { damping: 16, stiffness: 60 },
  });
  const animatedValue = Math.round(valueProgress * value);

  return (
    <AbsoluteFill
      style={{
        fontFamily,
        backgroundColor: "#09090b",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        gap: 24,
        opacity: containerOpacity,
      }}
    >
      <div
        style={{
          backgroundColor: `${accentColor}22`,
          border: `1px solid ${accentColor}44`,
          color: accentColor,
          fontSize: 24,
          fontWeight: 600,
          padding: "8px 20px",
          borderRadius: 100,
        }}
      >
        {badgeLabel}
      </div>

      <p style={{ color: "#71717a", fontSize: 32, margin: 0 }}>
        Hi, {recipientName}
      </p>

      <div style={{ textAlign: "center", transform: `scale(${nameScale})` }}>
        <span
          style={{
            fontSize: 120,
            fontWeight: 700,
            color: accentColor,
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {animatedValue.toLocaleString()}
        </span>
        <span style={{ fontSize: 48, color: "#a1a1aa", marginLeft: 12 }}>
          {unit}
        </span>
      </div>

      <p style={{ color: "#52525b", fontSize: 28, margin: 0 }}>{metric}</p>
    </AbsoluteFill>
  );
};
```
