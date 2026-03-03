/**
 * explainer.tsx — Parametric tech explainer template.
 *
 * Structure: Title card → N content sections → Summary card
 * Each section has a heading, body text, and optional icon.
 *
 * Usage:
 *   Register in Root.tsx as <Composition id="Explainer" component={Explainer} ... />
 *   Adjust defaultProps to match your content.
 *
 * Requires:
 *   npm install @remotion/google-fonts
 */

import React from 'react';
import { loadFont } from '@remotion/google-fonts/Inter';
import {
  AbsoluteFill,
  Composition,
  Sequence,
  Series,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { z } from 'zod';

// ── Font ─────────────────────────────────────────────────────────────────────

const { fontFamily } = loadFont('normal', {
  weights: ['400', '500', '600', '700'],
  subsets: ['latin'],
});

// ── Schema ───────────────────────────────────────────────────────────────────

const sectionSchema = z.object({
  heading: z.string(),
  body: z.string(),
  icon: z.string().optional(),
});

export const explainerSchema = z.object({
  title: z.string().default('How It Works'),
  tagline: z.string().default('A clear, step-by-step explanation.'),
  sections: z
    .array(sectionSchema)
    .default([
      { heading: 'Step 1', body: 'Describe the first concept or action here.', icon: '01' },
      { heading: 'Step 2', body: 'Describe the second concept or action here.', icon: '02' },
      { heading: 'Step 3', body: 'Describe the third concept or action here.', icon: '03' },
    ]),
  summaryTitle: z.string().default('That is all'),
  summaryBody: z.string().default('You now understand the full picture.'),
  accentColor: z.string().default('#6366f1'),
  backgroundColor: z.string().default('#09090b'),
  framesPerSection: z.number().int().min(30).default(120),
  titleFrames: z.number().int().min(30).default(90),
  summaryFrames: z.number().int().min(30).default(90),
});

export type ExplainerProps = z.infer<typeof explainerSchema>;

// ── Sub-components ────────────────────────────────────────────────────────────

const TitleCard: React.FC<Pick<ExplainerProps, 'title' | 'tagline' | 'accentColor' | 'backgroundColor'>> = ({
  title,
  tagline,
  accentColor,
  backgroundColor,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const titleScale = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  const taglineOpacity = interpolate(frame, [20, 45], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const exitOpacity = interpolate(frame, [durationInFrames - 15, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        fontFamily,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 24,
        opacity: exitOpacity,
      }}
    >
      {/* Accent line */}
      <div
        style={{
          width: 64,
          height: 4,
          backgroundColor: accentColor,
          borderRadius: 2,
          transform: `scaleX(${titleScale})`,
        }}
      />

      <h1
        style={{
          fontSize: 96,
          fontWeight: 700,
          color: '#fafafa',
          margin: 0,
          textAlign: 'center',
          letterSpacing: '-0.03em',
          lineHeight: 1.1,
          transform: `scale(${titleScale})`,
          padding: '0 80px',
        }}
      >
        {title}
      </h1>

      <p
        style={{
          fontSize: 36,
          fontWeight: 400,
          color: '#71717a',
          margin: 0,
          textAlign: 'center',
          maxWidth: 800,
          opacity: taglineOpacity,
          padding: '0 80px',
        }}
      >
        {tagline}
      </p>
    </AbsoluteFill>
  );
};

const SectionCard: React.FC<{
  heading: string;
  body: string;
  icon?: string;
  accentColor: string;
  backgroundColor: string;
  index: number;
  total: number;
}> = ({ heading, body, icon, accentColor, backgroundColor, index, total }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const iconScale = spring({ frame, fps, config: { damping: 12, stiffness: 100 } });
  const contentOpacity = interpolate(frame, [15, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const contentY = interpolate(frame, [15, 40], [20, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const exitOpacity = interpolate(frame, [durationInFrames - 15, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        fontFamily,
        justifyContent: 'center',
        alignItems: 'flex-start',
        padding: '0 140px',
        gap: 0,
        opacity: exitOpacity,
      }}
    >
      {/* Progress indicator */}
      <div
        style={{
          position: 'absolute',
          top: 60,
          left: 140,
          display: 'flex',
          gap: 8,
        }}
      >
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            style={{
              width: i === index ? 32 : 8,
              height: 4,
              borderRadius: 2,
              backgroundColor: i === index ? accentColor : '#27272a',
              transition: 'none',
            }}
          />
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 32, maxWidth: 1000 }}>
        {/* Icon / number */}
        {icon && (
          <div
            style={{
              fontSize: 80,
              fontWeight: 700,
              color: accentColor,
              lineHeight: 1,
              transform: `scale(${iconScale})`,
              transformOrigin: 'left center',
            }}
          >
            {icon}
          </div>
        )}

        {/* Heading */}
        <h2
          style={{
            fontSize: 72,
            fontWeight: 700,
            color: '#fafafa',
            margin: 0,
            letterSpacing: '-0.025em',
            lineHeight: 1.1,
            opacity: contentOpacity,
            transform: `translateY(${contentY}px)`,
          }}
        >
          {heading}
        </h2>

        {/* Body */}
        <p
          style={{
            fontSize: 36,
            fontWeight: 400,
            color: '#a1a1aa',
            margin: 0,
            lineHeight: 1.6,
            maxWidth: 800,
            opacity: contentOpacity,
            transform: `translateY(${contentY}px)`,
          }}
        >
          {body}
        </p>
      </div>
    </AbsoluteFill>
  );
};

const SummaryCard: React.FC<
  Pick<ExplainerProps, 'summaryTitle' | 'summaryBody' | 'accentColor' | 'backgroundColor'>
> = ({ summaryTitle, summaryBody, accentColor, backgroundColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 80 } });
  const bodyOpacity = interpolate(frame, [20, 50], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        fontFamily,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 32,
        padding: '0 120px',
      }}
    >
      {/* Checkmark */}
      <div
        style={{
          width: 80,
          height: 80,
          borderRadius: '50%',
          backgroundColor: `${accentColor}22`,
          border: `3px solid ${accentColor}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 36,
          transform: `scale(${scale})`,
        }}
      >
        ✓
      </div>

      <h2
        style={{
          fontSize: 80,
          fontWeight: 700,
          color: '#fafafa',
          margin: 0,
          textAlign: 'center',
          letterSpacing: '-0.025em',
          transform: `scale(${scale})`,
        }}
      >
        {summaryTitle}
      </h2>

      <p
        style={{
          fontSize: 36,
          color: '#71717a',
          margin: 0,
          textAlign: 'center',
          maxWidth: 700,
          lineHeight: 1.5,
          opacity: bodyOpacity,
        }}
      >
        {summaryBody}
      </p>
    </AbsoluteFill>
  );
};

// ── Main composition ──────────────────────────────────────────────────────────

export const Explainer: React.FC<ExplainerProps> = ({
  title,
  tagline,
  sections,
  summaryTitle,
  summaryBody,
  accentColor,
  backgroundColor,
  framesPerSection,
  titleFrames,
  summaryFrames,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor }}>
      <Series>
        <Series.Sequence durationInFrames={titleFrames}>
          <TitleCard title={title} tagline={tagline} accentColor={accentColor} backgroundColor={backgroundColor} />
        </Series.Sequence>

        {sections.map((section, i) => (
          <Series.Sequence key={i} durationInFrames={framesPerSection}>
            <SectionCard
              heading={section.heading}
              body={section.body}
              icon={section.icon}
              accentColor={accentColor}
              backgroundColor={backgroundColor}
              index={i}
              total={sections.length}
            />
          </Series.Sequence>
        ))}

        <Series.Sequence durationInFrames={summaryFrames}>
          <SummaryCard
            summaryTitle={summaryTitle}
            summaryBody={summaryBody}
            accentColor={accentColor}
            backgroundColor={backgroundColor}
          />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};

// ── Root registration (copy to your Root.tsx) ─────────────────────────────────

export const ExplainerRoot: React.FC = () => {
  const defaultProps: ExplainerProps = {
    title: 'How It Works',
    tagline: 'Three steps to get started.',
    sections: [
      { heading: 'Connect', body: 'Integrate with your existing tools in minutes.', icon: '01' },
      { heading: 'Configure', body: 'Set up your workflow with a simple config file.', icon: '02' },
      { heading: 'Ship', body: 'Deploy to production with one command.', icon: '03' },
    ],
    summaryTitle: "You're ready",
    summaryBody: 'Start building your first video today.',
    accentColor: '#6366f1',
    backgroundColor: '#09090b',
    framesPerSection: 120,
    titleFrames: 90,
    summaryFrames: 90,
  };

  const totalFrames =
    defaultProps.titleFrames +
    defaultProps.sections.length * defaultProps.framesPerSection +
    defaultProps.summaryFrames;

  return (
    <Composition
      id="Explainer"
      component={Explainer}
      schema={explainerSchema}
      defaultProps={defaultProps}
      durationInFrames={totalFrames}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
