/**
 * data-viz.tsx — Animated chart composition template.
 *
 * Structure: Data intro → Animated bar chart → Callouts / insights
 * Config-driven: all data and labels via props.
 *
 * Usage:
 *   Register in Root.tsx as <Composition id="DataViz" component={DataViz} ... />
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
  interpolateColors,
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

const datumSchema = z.object({
  label: z.string(),
  value: z.number(),
  color: z.string().optional(),
});

const calloutSchema = z.object({
  headline: z.string(),
  body: z.string(),
  accentIcon: z.string().optional(),
});

export const dataVizSchema = z.object({
  // Intro
  introTitle: z.string().default('The Numbers'),
  introSubtitle: z.string().default('Key metrics at a glance.'),
  introFrames: z.number().int().min(30).default(75),

  // Chart
  chartTitle: z.string().default('Performance by Category'),
  chartSubtitle: z.string().optional(),
  data: z
    .array(datumSchema)
    .default([
      { label: 'Q1', value: 42, color: '#6366f1' },
      { label: 'Q2', value: 67, color: '#8b5cf6' },
      { label: 'Q3', value: 55, color: '#a78bfa' },
      { label: 'Q4', value: 91, color: '#6366f1' },
    ]),
  valueUnit: z.string().default('%'),
  chartFrames: z.number().int().min(60).default(150),

  // Callouts
  callouts: z
    .array(calloutSchema)
    .default([
      { headline: '+48%', body: 'YoY growth in Q4', accentIcon: '↑' },
      { headline: '91%', body: 'Peak performance', accentIcon: '★' },
    ]),
  calloutFrames: z.number().int().min(30).default(100),

  // Branding
  accentColor: z.string().default('#6366f1'),
  backgroundColor: z.string().default('#09090b'),
  gridColor: z.string().default('#27272a'),
});

export type DataVizProps = z.infer<typeof dataVizSchema>;
type Datum = z.infer<typeof datumSchema>;
type Callout = z.infer<typeof calloutSchema>;

// ── Intro scene ───────────────────────────────────────────────────────────────

const IntroScene: React.FC<{
  introTitle: string;
  introSubtitle: string;
  accentColor: string;
  backgroundColor: string;
}> = ({ introTitle, introSubtitle, accentColor, backgroundColor }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const lineScale = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  const titleOpacity = interpolate(frame, [8, 30], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const titleY = interpolate(frame, [8, 30], [30, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const subtitleOpacity = interpolate(frame, [25, 50], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
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
      <div
        style={{
          width: 80,
          height: 4,
          backgroundColor: accentColor,
          borderRadius: 2,
          transform: `scaleX(${lineScale})`,
        }}
      />
      <h1
        style={{
          fontSize: 96,
          fontWeight: 700,
          color: '#fafafa',
          margin: 0,
          letterSpacing: '-0.03em',
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
        }}
      >
        {introTitle}
      </h1>
      <p
        style={{
          fontSize: 36,
          color: '#71717a',
          margin: 0,
          opacity: subtitleOpacity,
        }}
      >
        {introSubtitle}
      </p>
    </AbsoluteFill>
  );
};

// ── Chart scene ───────────────────────────────────────────────────────────────

const CHART_HEIGHT = 480;
const CHART_BAR_WIDTH = 100;

const Bar: React.FC<{
  datum: Datum;
  maxValue: number;
  index: number;
  accentColor: string;
}> = ({ datum, maxValue, index, accentColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = index * 6;
  const progress = spring({
    frame: Math.max(0, frame - delay),
    fps,
    config: { damping: 14, stiffness: 80 },
  });

  const barColor = datum.color ?? accentColor;
  const barHeight = (datum.value / maxValue) * CHART_HEIGHT * progress;

  const labelOpacity = interpolate(frame, [delay + 10, delay + 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 12,
        width: CHART_BAR_WIDTH + 40,
      }}
    >
      {/* Value label above bar */}
      <span
        style={{
          fontSize: 26,
          fontWeight: 700,
          color: barColor,
          opacity: labelOpacity,
          fontVariantNumeric: 'tabular-nums',
          minHeight: 36,
          display: 'flex',
          alignItems: 'flex-end',
        }}
      >
        {Math.round(datum.value * progress)}
      </span>

      {/* Bar */}
      <div
        style={{
          width: CHART_BAR_WIDTH,
          height: barHeight,
          backgroundColor: barColor,
          borderRadius: '8px 8px 0 0',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Shine effect */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '30%',
            background: 'linear-gradient(180deg, rgba(255,255,255,0.15) 0%, transparent 100%)',
            borderRadius: '8px 8px 0 0',
          }}
        />
      </div>

      {/* X-axis label */}
      <span
        style={{
          fontSize: 22,
          color: '#71717a',
          fontWeight: 500,
          opacity: labelOpacity,
        }}
      >
        {datum.label}
      </span>
    </div>
  );
};

const ChartScene: React.FC<{
  chartTitle: string;
  chartSubtitle?: string;
  data: Datum[];
  valueUnit: string;
  accentColor: string;
  backgroundColor: string;
  gridColor: string;
}> = ({ chartTitle, chartSubtitle, data, valueUnit, accentColor, backgroundColor, gridColor }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const maxValue = Math.max(...data.map((d) => d.value));
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const exitOpacity = interpolate(frame, [durationInFrames - 15, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const gridLines = [0, 0.25, 0.5, 0.75, 1];

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        fontFamily,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        padding: '60px 100px',
        gap: 40,
        opacity: exitOpacity,
      }}
    >
      {/* Title block */}
      <div style={{ width: '100%', opacity: titleOpacity }}>
        <h2
          style={{
            fontSize: 56,
            fontWeight: 700,
            color: '#fafafa',
            margin: 0,
            letterSpacing: '-0.02em',
          }}
        >
          {chartTitle}
        </h2>
        {chartSubtitle && (
          <p style={{ fontSize: 28, color: '#71717a', margin: '8px 0 0', fontWeight: 400 }}>
            {chartSubtitle}
          </p>
        )}
      </div>

      {/* Chart area */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'center',
          gap: 40,
          height: CHART_HEIGHT + 80,
          paddingBottom: 0,
        }}
      >
        {/* Grid lines */}
        {gridLines.map((t) => {
          const y = CHART_HEIGHT - t * CHART_HEIGHT;
          const label = Math.round(t * maxValue);
          return (
            <React.Fragment key={t}>
              <div
                style={{
                  position: 'absolute',
                  left: 60,
                  right: 0,
                  top: y,
                  height: 1,
                  backgroundColor: gridColor,
                  opacity: t === 0 ? 1 : 0.5,
                }}
              />
              {t > 0 && (
                <span
                  style={{
                    position: 'absolute',
                    left: 0,
                    top: y - 14,
                    fontSize: 20,
                    color: '#52525b',
                    width: 50,
                    textAlign: 'right',
                    fontVariantNumeric: 'tabular-nums',
                  }}
                >
                  {label}
                </span>
              )}
            </React.Fragment>
          );
        })}

        {/* Bars */}
        <div
          style={{
            display: 'flex',
            alignItems: 'flex-end',
            gap: 40,
            height: CHART_HEIGHT,
            paddingLeft: 70,
          }}
        >
          {data.map((d, i) => (
            <Bar key={i} datum={d} maxValue={maxValue} index={i} accentColor={accentColor} />
          ))}
        </div>
      </div>

      {/* Unit label */}
      <p style={{ fontSize: 22, color: '#52525b', margin: 0, alignSelf: 'flex-end' }}>
        Values in {valueUnit}
      </p>
    </AbsoluteFill>
  );
};

// ── Callouts scene ────────────────────────────────────────────────────────────

const CalloutCard: React.FC<{ callout: Callout; index: number; accentColor: string }> = ({
  callout,
  index,
  accentColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = index * 12;
  const scale = spring({ frame: Math.max(0, frame - delay), fps, config: { damping: 14, stiffness: 100 } });
  const bodyOpacity = interpolate(frame, [delay + 15, delay + 35], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        backgroundColor: '#18181b',
        border: `1px solid ${accentColor}30`,
        borderRadius: 20,
        padding: '48px 56px',
        display: 'flex',
        flexDirection: 'column',
        gap: 16,
        flex: 1,
        transform: `scale(${scale})`,
      }}
    >
      {callout.accentIcon && (
        <div style={{ fontSize: 48, color: accentColor, lineHeight: 1 }}>{callout.accentIcon}</div>
      )}
      <div
        style={{
          fontSize: 80,
          fontWeight: 700,
          color: accentColor,
          lineHeight: 1,
          letterSpacing: '-0.03em',
        }}
      >
        {callout.headline}
      </div>
      <p
        style={{
          fontSize: 30,
          color: '#a1a1aa',
          margin: 0,
          lineHeight: 1.4,
          opacity: bodyOpacity,
        }}
      >
        {callout.body}
      </p>
    </div>
  );
};

const CalloutsScene: React.FC<{
  callouts: Callout[];
  accentColor: string;
  backgroundColor: string;
}> = ({ callouts, accentColor, backgroundColor }) => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        fontFamily,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        padding: '80px 120px',
        gap: 56,
      }}
    >
      <h2
        style={{
          fontSize: 52,
          fontWeight: 700,
          color: '#fafafa',
          margin: 0,
          textAlign: 'center',
          letterSpacing: '-0.02em',
          opacity: titleOpacity,
        }}
      >
        Key Insights
      </h2>

      <div style={{ display: 'flex', gap: 40, width: '100%' }}>
        {callouts.map((c, i) => (
          <CalloutCard key={i} callout={c} index={i} accentColor={accentColor} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ── Main composition ──────────────────────────────────────────────────────────

export const DataViz: React.FC<DataVizProps> = ({
  introTitle,
  introSubtitle,
  introFrames,
  chartTitle,
  chartSubtitle,
  data,
  valueUnit,
  chartFrames,
  callouts,
  calloutFrames,
  accentColor,
  backgroundColor,
  gridColor,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor }}>
      <Series>
        <Series.Sequence durationInFrames={introFrames}>
          <IntroScene
            introTitle={introTitle}
            introSubtitle={introSubtitle}
            accentColor={accentColor}
            backgroundColor={backgroundColor}
          />
        </Series.Sequence>

        <Series.Sequence durationInFrames={chartFrames}>
          <ChartScene
            chartTitle={chartTitle}
            chartSubtitle={chartSubtitle}
            data={data}
            valueUnit={valueUnit}
            accentColor={accentColor}
            backgroundColor={backgroundColor}
            gridColor={gridColor}
          />
        </Series.Sequence>

        <Series.Sequence durationInFrames={calloutFrames}>
          <CalloutsScene callouts={callouts} accentColor={accentColor} backgroundColor={backgroundColor} />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};

// ── Root registration (copy to your Root.tsx) ─────────────────────────────────

export const DataVizRoot: React.FC = () => {
  const defaultProps: DataVizProps = {
    introTitle: 'The Numbers',
    introSubtitle: 'Key metrics at a glance.',
    introFrames: 75,
    chartTitle: 'Performance by Quarter',
    chartSubtitle: 'FY 2025 results',
    data: [
      { label: 'Q1', value: 42, color: '#6366f1' },
      { label: 'Q2', value: 67, color: '#8b5cf6' },
      { label: 'Q3', value: 55, color: '#a78bfa' },
      { label: 'Q4', value: 91, color: '#6366f1' },
    ],
    valueUnit: '%',
    chartFrames: 150,
    callouts: [
      { headline: '+48%', body: 'YoY growth in Q4', accentIcon: '↑' },
      { headline: '91%', body: 'Peak performance this year', accentIcon: '★' },
    ],
    calloutFrames: 100,
    accentColor: '#6366f1',
    backgroundColor: '#09090b',
    gridColor: '#27272a',
  };

  const totalFrames = defaultProps.introFrames + defaultProps.chartFrames + defaultProps.calloutFrames;

  return (
    <Composition
      id="DataViz"
      component={DataViz}
      schema={dataVizSchema}
      defaultProps={defaultProps}
      durationInFrames={totalFrames}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
