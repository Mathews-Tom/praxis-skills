# Remotion Charts

Bar, pie, line, and chart animation patterns — built with pure React/CSS, no charting library required.

## Animated Bar Chart

```tsx
import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

type BarDatum = { label: string; value: number; color: string };

type BarChartProps = {
  data: BarDatum[];
  title: string;
};

const CHART_HEIGHT = 400;

export const BarChart: React.FC<BarChartProps> = ({ data, title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const maxValue = Math.max(...data.map((d) => d.value));

  return (
    <AbsoluteFill style={{
      backgroundColor: '#09090b',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
      padding: 80,
      gap: 40,
    }}>
      <h2 style={{ color: '#fafafa', fontSize: 48, fontWeight: 700, margin: 0 }}>{title}</h2>

      <div style={{ display: 'flex', alignItems: 'flex-end', gap: 24, height: CHART_HEIGHT }}>
        {data.map((d, i) => {
          const delay = i * 5;
          const progress = spring({
            frame: Math.max(0, frame - delay),
            fps,
            config: { damping: 14, stiffness: 80 },
          });
          const barHeight = (d.value / maxValue) * CHART_HEIGHT * progress;
          const labelOpacity = interpolate(frame, [delay + 10, delay + 25], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          });

          return (
            <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12, width: 100 }}>
              <span style={{ color: '#fafafa', fontSize: 24, fontWeight: 600, opacity: labelOpacity }}>
                {d.value}
              </span>
              <div style={{
                width: 80,
                height: barHeight,
                backgroundColor: d.color,
                borderRadius: '6px 6px 0 0',
                transition: 'none',
              }} />
              <span style={{ color: '#71717a', fontSize: 20, textAlign: 'center', opacity: labelOpacity }}>
                {d.label}
              </span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

## Animated Pie/Donut Chart

Use SVG `stroke-dasharray`/`stroke-dashoffset` to animate a donut chart:

```tsx
type PieSlice = { label: string; value: number; color: string };

type DonutChartProps = {
  data: PieSlice[];
  title: string;
};

export const DonutChart: React.FC<DonutChartProps> = ({ data, title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const SIZE = 400;
  const STROKE_WIDTH = 60;
  const RADIUS = (SIZE - STROKE_WIDTH) / 2;
  const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

  const total = data.reduce((sum, d) => sum + d.value, 0);
  const progress = spring({ frame, fps, config: { damping: 14, stiffness: 60 } });

  let offset = 0;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#09090b', flexDirection: 'column', gap: 40 }}>
      <h2 style={{ color: '#fafafa', fontSize: 48, fontWeight: 700, margin: 0 }}>{title}</h2>

      <div style={{ position: 'relative', width: SIZE, height: SIZE }}>
        <svg width={SIZE} height={SIZE} style={{ transform: 'rotate(-90deg)' }}>
          {data.map((slice, i) => {
            const sliceFraction = slice.value / total;
            const sliceLength = CIRCUMFERENCE * sliceFraction * progress;
            const currentOffset = CIRCUMFERENCE - offset * CIRCUMFERENCE;

            const el = (
              <circle
                key={i}
                cx={SIZE / 2}
                cy={SIZE / 2}
                r={RADIUS}
                fill="none"
                stroke={slice.color}
                strokeWidth={STROKE_WIDTH}
                strokeDasharray={`${sliceLength} ${CIRCUMFERENCE}`}
                strokeDashoffset={currentOffset}
              />
            );

            offset += sliceFraction;
            return el;
          })}
        </svg>

        {/* Center label */}
        <div style={{
          position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
          display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        }}>
          <span style={{ color: '#fafafa', fontSize: 48, fontWeight: 700 }}>{total}</span>
          <span style={{ color: '#71717a', fontSize: 20 }}>Total</span>
        </div>
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', gap: 24 }}>
        {data.map((d, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div style={{ width: 16, height: 16, backgroundColor: d.color, borderRadius: 4 }} />
            <span style={{ color: '#a1a1aa', fontSize: 24 }}>{d.label}</span>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

## Animated Line Chart

Use SVG `stroke-dasharray` clipping to animate a line being drawn:

```tsx
type LinePoint = { x: number; y: number };

type LineChartProps = {
  points: LinePoint[];
  title: string;
  lineColor?: string;
};

export const LineChart: React.FC<LineChartProps> = ({ points, title, lineColor = '#6366f1' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const W = 900;
  const H = 400;
  const PADDING = 60;

  const maxX = Math.max(...points.map((p) => p.x));
  const maxY = Math.max(...points.map((p) => p.y));
  const minY = Math.min(...points.map((p) => p.y));

  const toSvg = (p: LinePoint) => ({
    x: PADDING + (p.x / maxX) * (W - PADDING * 2),
    y: H - PADDING - ((p.y - minY) / (maxY - minY || 1)) * (H - PADDING * 2),
  });

  const svgPoints = points.map(toSvg);
  const pathD = svgPoints.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');

  // Approximate path length
  const pathLength = svgPoints.reduce((sum, p, i) => {
    if (i === 0) return 0;
    const prev = svgPoints[i - 1];
    return sum + Math.hypot(p.x - prev.x, p.y - prev.y);
  }, 0);

  const drawProgress = spring({ frame, fps, config: { damping: 20, stiffness: 50 } });
  const drawnLength = pathLength * drawProgress;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#09090b', flexDirection: 'column', gap: 32 }}>
      <h2 style={{ color: '#fafafa', fontSize: 48, fontWeight: 700, margin: 0 }}>{title}</h2>
      <svg width={W} height={H}>
        {/* Grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((t) => {
          const y = PADDING + (1 - t) * (H - PADDING * 2);
          return (
            <line key={t} x1={PADDING} x2={W - PADDING} y1={y} y2={y}
              stroke="#27272a" strokeWidth={1} strokeDasharray="4 4" />
          );
        })}
        {/* Animated path */}
        <path
          d={pathD}
          fill="none"
          stroke={lineColor}
          strokeWidth={3}
          strokeDasharray={`${drawnLength} ${pathLength}`}
          strokeDashoffset={0}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {/* Data points */}
        {svgPoints.map((p, i) => {
          const pointDelay = (i / svgPoints.length) * 60;
          const pointOpacity = interpolate(frame, [pointDelay, pointDelay + 10], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          });
          return (
            <circle key={i} cx={p.x} cy={p.y} r={6}
              fill={lineColor} opacity={pointOpacity} />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
```

## Number Counter Animation

Animate a number from 0 to a target value:

```tsx
type CounterProps = {
  target: number;
  prefix?: string;
  suffix?: string;
  durationFrames?: number;
};

export const Counter: React.FC<CounterProps> = ({ target, prefix = '', suffix = '', durationFrames = 60 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, config: { damping: 18, stiffness: 60 } });
  const value = Math.round(progress * target);

  return (
    <div style={{ fontSize: 96, fontWeight: 700, color: '#fafafa', fontVariantNumeric: 'tabular-nums' }}>
      {prefix}{value.toLocaleString()}{suffix}
    </div>
  );
};
```
