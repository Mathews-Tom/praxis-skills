/**
 * product-demo.tsx — Product showcase template.
 *
 * Structure: Hero → Feature cards → CTA
 * Config-driven: all content via props.
 *
 * Usage:
 *   Register in Root.tsx as <Composition id="ProductDemo" component={ProductDemo} ... />
 *
 * Requires:
 *   npm install @remotion/google-fonts
 */

import React from 'react';
import { loadFont } from '@remotion/google-fonts/Inter';
import {
  AbsoluteFill,
  Composition,
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

const featureSchema = z.object({
  icon: z.string(),
  title: z.string(),
  description: z.string(),
});

export const productDemoSchema = z.object({
  // Hero
  badgeLabel: z.string().default('Introducing'),
  productName: z.string().default('Product Name'),
  heroTagline: z.string().default('The fastest way to do the thing.'),
  heroFrames: z.number().int().min(30).default(90),

  // Features
  featuresTitle: z.string().default('Everything you need'),
  features: z
    .array(featureSchema)
    .default([
      { icon: '⚡', title: 'Lightning Fast', description: 'Renders in milliseconds, not seconds.' },
      { icon: '🎨', title: 'Fully Customizable', description: 'Every pixel under your control.' },
      { icon: '🔒', title: 'Secure by Default', description: 'Enterprise-grade security built in.' },
      { icon: '📦', title: 'Zero Config', description: 'Works out of the box. No setup needed.' },
      { icon: '🌍', title: 'Global CDN', description: 'Sub-100ms delivery worldwide.' },
      { icon: '📈', title: 'Analytics', description: 'Real-time insights on every video.' },
    ]),
  featuresFrames: z.number().int().min(30).default(150),

  // CTA
  ctaHeadline: z.string().default('Start for free'),
  ctaSubtext: z.string().default('No credit card required. Ready in 30 seconds.'),
  ctaButtonLabel: z.string().default('Get started →'),
  ctaFrames: z.number().int().min(30).default(90),

  // Branding
  accentColor: z.string().default('#6366f1'),
  accentColorDark: z.string().default('#4338ca'),
  backgroundColor: z.string().default('#09090b'),
});

export type ProductDemoProps = z.infer<typeof productDemoSchema>;

// ── Hero ──────────────────────────────────────────────────────────────────────

const HeroScene: React.FC<{
  badgeLabel: string;
  productName: string;
  heroTagline: string;
  accentColor: string;
  backgroundColor: string;
}> = ({ badgeLabel, productName, heroTagline, accentColor, backgroundColor }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const badgeOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  const nameScale = spring({ frame: Math.max(0, frame - 8), fps, config: { damping: 12, stiffness: 100 } });
  const taglineOpacity = interpolate(frame, [25, 50], [0, 1], {
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
        gap: 32,
        padding: '0 120px',
        opacity: exitOpacity,
      }}
    >
      {/* Background gradient */}
      <div
        style={{
          position: 'absolute',
          top: -200,
          left: '50%',
          transform: 'translateX(-50%)',
          width: 800,
          height: 800,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${accentColor}18 0%, transparent 70%)`,
          pointerEvents: 'none',
        }}
      />

      {/* Badge */}
      <div
        style={{
          backgroundColor: `${accentColor}20`,
          border: `1px solid ${accentColor}40`,
          color: accentColor,
          fontSize: 22,
          fontWeight: 600,
          padding: '8px 20px',
          borderRadius: 100,
          opacity: badgeOpacity,
          letterSpacing: '0.05em',
          textTransform: 'uppercase',
        }}
      >
        {badgeLabel}
      </div>

      {/* Product name */}
      <h1
        style={{
          fontSize: 120,
          fontWeight: 700,
          color: '#fafafa',
          margin: 0,
          textAlign: 'center',
          letterSpacing: '-0.04em',
          lineHeight: 1.0,
          transform: `scale(${nameScale})`,
        }}
      >
        {productName}
      </h1>

      {/* Tagline */}
      <p
        style={{
          fontSize: 40,
          fontWeight: 400,
          color: '#71717a',
          margin: 0,
          textAlign: 'center',
          maxWidth: 900,
          lineHeight: 1.4,
          opacity: taglineOpacity,
        }}
      >
        {heroTagline}
      </p>
    </AbsoluteFill>
  );
};

// ── Features ──────────────────────────────────────────────────────────────────

type Feature = z.infer<typeof featureSchema>;

const FeatureCard: React.FC<{ feature: Feature; index: number; accentColor: string }> = ({
  feature,
  index,
  accentColor,
}) => {
  const frame = useCurrentFrame();
  const delay = index * 6;
  const opacity = interpolate(frame, [delay, delay + 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const y = interpolate(frame, [delay, delay + 20], [30, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        backgroundColor: '#18181b',
        border: '1px solid #27272a',
        borderRadius: 16,
        padding: '32px 28px',
        display: 'flex',
        flexDirection: 'column',
        gap: 12,
        opacity,
        transform: `translateY(${y}px)`,
      }}
    >
      <div style={{ fontSize: 40 }}>{feature.icon}</div>
      <h3 style={{ fontSize: 26, fontWeight: 600, color: '#fafafa', margin: 0 }}>{feature.title}</h3>
      <p style={{ fontSize: 20, color: '#71717a', margin: 0, lineHeight: 1.5 }}>{feature.description}</p>
    </div>
  );
};

const FeaturesScene: React.FC<{
  featuresTitle: string;
  features: Feature[];
  accentColor: string;
  backgroundColor: string;
}> = ({ featuresTitle, features, accentColor, backgroundColor }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const exitOpacity = interpolate(frame, [durationInFrames - 15, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const cols = features.length <= 3 ? features.length : 3;

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        fontFamily,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 48,
        padding: '60px 100px',
        opacity: exitOpacity,
      }}
    >
      <h2
        style={{
          fontSize: 56,
          fontWeight: 700,
          color: '#fafafa',
          margin: 0,
          textAlign: 'center',
          letterSpacing: '-0.025em',
          opacity: titleOpacity,
        }}
      >
        {featuresTitle}
      </h2>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${cols}, 1fr)`,
          gap: 24,
          width: '100%',
        }}
      >
        {features.map((f, i) => (
          <FeatureCard key={i} feature={f} index={i} accentColor={accentColor} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ── CTA ───────────────────────────────────────────────────────────────────────

const CTAScene: React.FC<{
  ctaHeadline: string;
  ctaSubtext: string;
  ctaButtonLabel: string;
  accentColor: string;
  accentColorDark: string;
  backgroundColor: string;
}> = ({ ctaHeadline, ctaSubtext, ctaButtonLabel, accentColor, accentColorDark, backgroundColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 90 } });
  const subtextOpacity = interpolate(frame, [20, 45], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const buttonOpacity = interpolate(frame, [35, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const buttonScale = spring({
    frame: Math.max(0, frame - 35),
    fps,
    config: { damping: 12, stiffness: 120 },
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
      {/* Background glow */}
      <div
        style={{
          position: 'absolute',
          bottom: -200,
          left: '50%',
          transform: 'translateX(-50%)',
          width: 600,
          height: 600,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${accentColor}20 0%, transparent 70%)`,
          pointerEvents: 'none',
        }}
      />

      <h2
        style={{
          fontSize: 96,
          fontWeight: 700,
          color: '#fafafa',
          margin: 0,
          textAlign: 'center',
          letterSpacing: '-0.035em',
          lineHeight: 1.05,
          transform: `scale(${scale})`,
        }}
      >
        {ctaHeadline}
      </h2>

      <p
        style={{
          fontSize: 32,
          color: '#71717a',
          margin: 0,
          textAlign: 'center',
          maxWidth: 600,
          opacity: subtextOpacity,
        }}
      >
        {ctaSubtext}
      </p>

      <button
        style={{
          background: `linear-gradient(135deg, ${accentColor}, ${accentColorDark})`,
          color: '#ffffff',
          fontSize: 28,
          fontWeight: 600,
          padding: '20px 48px',
          borderRadius: 14,
          border: 'none',
          cursor: 'default',
          opacity: buttonOpacity,
          transform: `scale(${buttonScale})`,
          fontFamily,
          letterSpacing: '-0.01em',
        }}
      >
        {ctaButtonLabel}
      </button>
    </AbsoluteFill>
  );
};

// ── Main composition ──────────────────────────────────────────────────────────

export const ProductDemo: React.FC<ProductDemoProps> = ({
  badgeLabel,
  productName,
  heroTagline,
  heroFrames,
  featuresTitle,
  features,
  featuresFrames,
  ctaHeadline,
  ctaSubtext,
  ctaButtonLabel,
  ctaFrames,
  accentColor,
  accentColorDark,
  backgroundColor,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor }}>
      <Series>
        <Series.Sequence durationInFrames={heroFrames}>
          <HeroScene
            badgeLabel={badgeLabel}
            productName={productName}
            heroTagline={heroTagline}
            accentColor={accentColor}
            backgroundColor={backgroundColor}
          />
        </Series.Sequence>

        <Series.Sequence durationInFrames={featuresFrames}>
          <FeaturesScene
            featuresTitle={featuresTitle}
            features={features}
            accentColor={accentColor}
            backgroundColor={backgroundColor}
          />
        </Series.Sequence>

        <Series.Sequence durationInFrames={ctaFrames}>
          <CTAScene
            ctaHeadline={ctaHeadline}
            ctaSubtext={ctaSubtext}
            ctaButtonLabel={ctaButtonLabel}
            accentColor={accentColor}
            accentColorDark={accentColorDark}
            backgroundColor={backgroundColor}
          />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};

// ── Root registration (copy to your Root.tsx) ─────────────────────────────────

export const ProductDemoRoot: React.FC = () => {
  const defaultProps: ProductDemoProps = {
    badgeLabel: 'Introducing',
    productName: 'Product Name',
    heroTagline: 'The fastest way to do the thing.',
    heroFrames: 90,
    featuresTitle: 'Everything you need',
    features: [
      { icon: '⚡', title: 'Lightning Fast', description: 'Renders in milliseconds, not seconds.' },
      { icon: '🎨', title: 'Fully Customizable', description: 'Every pixel under your control.' },
      { icon: '🔒', title: 'Secure by Default', description: 'Enterprise-grade security built in.' },
      { icon: '📦', title: 'Zero Config', description: 'Works out of the box. No setup needed.' },
      { icon: '🌍', title: 'Global CDN', description: 'Sub-100ms delivery worldwide.' },
      { icon: '📈', title: 'Analytics', description: 'Real-time insights on every video.' },
    ],
    featuresFrames: 150,
    ctaHeadline: 'Start for free',
    ctaSubtext: 'No credit card required. Ready in 30 seconds.',
    ctaButtonLabel: 'Get started →',
    ctaFrames: 90,
    accentColor: '#6366f1',
    accentColorDark: '#4338ca',
    backgroundColor: '#09090b',
  };

  const totalFrames = defaultProps.heroFrames + defaultProps.featuresFrames + defaultProps.ctaFrames;

  return (
    <Composition
      id="ProductDemo"
      component={ProductDemo}
      schema={productDemoSchema}
      defaultProps={defaultProps}
      durationInFrames={totalFrames}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
