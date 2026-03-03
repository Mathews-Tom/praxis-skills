# Remotion 3D with @remotion/three

Three.js integration via React Three Fiber and @remotion/three for 3D scenes in videos.

## Setup

Install dependencies:

```bash
npm install @remotion/three three @react-three/fiber @react-three/drei
npm install --save-dev @types/three
```

## ThreeCanvas

`ThreeCanvas` is a Remotion-aware wrapper around React Three Fiber's `Canvas`. It hooks into Remotion's frame system to make Three.js animations frame-deterministic.

```tsx
import { ThreeCanvas } from '@remotion/three';
import { AbsoluteFill, useVideoConfig } from 'remotion';

const ThreeScene: React.FC = () => {
  const { width, height } = useVideoConfig();

  return (
    <AbsoluteFill>
      <ThreeCanvas width={width} height={height}>
        {/* Three.js scene graph here */}
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <mesh>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="#6366f1" />
        </mesh>
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
```

Never use `useFrame` from `@react-three/fiber` inside Remotion — it uses wall-clock time. Instead, drive animations via `useCurrentFrame()` and pass derived values to Three.js objects.

## Animating 3D Objects

Pass frame-derived values as props to meshes and lights:

```tsx
import { ThreeCanvas } from '@remotion/three';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useRef } from 'react';
import * as THREE from 'three';

const RotatingCube: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Rotation derived from frame
  const rotationY = interpolate(frame, [0, 150], [0, Math.PI * 2]);
  const rotationX = interpolate(frame, [0, 150], [0, Math.PI * 0.5]);

  // Scale spring on entry
  const scale = spring({ frame, fps, config: { damping: 12, stiffness: 100 } });

  return (
    <mesh
      rotation={[rotationX, rotationY, 0]}
      scale={[scale, scale, scale]}
    >
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="#6366f1" roughness={0.4} metalness={0.6} />
    </mesh>
  );
};

export const CubeScene: React.FC = () => {
  const { width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#09090b' }}>
      <ThreeCanvas width={width} height={height}>
        <ambientLight intensity={0.3} />
        <directionalLight position={[5, 10, 7.5]} intensity={1} />
        <perspectiveCamera makeDefault position={[0, 0, 5]} fov={50} />
        <RotatingCube />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
```

## Camera Control

Set up a perspective camera explicitly for full control:

```tsx
import { PerspectiveCamera } from '@react-three/drei';
import { interpolate, useCurrentFrame } from 'remotion';

const AnimatedCamera: React.FC = () => {
  const frame = useCurrentFrame();
  const z = interpolate(frame, [0, 90], [10, 5], { extrapolateRight: 'clamp' });
  const y = interpolate(frame, [0, 90], [2, 0], { extrapolateRight: 'clamp' });

  return <PerspectiveCamera makeDefault position={[0, y, z]} fov={50} />;
};
```

## Lighting Patterns

```tsx
// Soft studio lighting
<>
  <ambientLight intensity={0.4} />
  <directionalLight position={[10, 10, 5]} intensity={0.8} castShadow />
  <directionalLight position={[-10, -5, -5]} intensity={0.3} color="#4466ff" />
</>

// Dramatic rim lighting
<>
  <ambientLight intensity={0.1} />
  <pointLight position={[5, 5, 5]} intensity={2} color="#ffffff" />
  <pointLight position={[-5, -5, 2]} intensity={0.5} color="#6366f1" />
  <pointLight position={[0, 5, -5]} intensity={0.3} color="#f59e0b" />
</>
```

## Using @react-three/drei Helpers

```tsx
import { Text, RoundedBox, Environment, Float } from '@react-three/drei';
import { useCurrentFrame, spring, useVideoConfig } from 'remotion';

const FloatingCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 80 } });

  return (
    <Float speed={0} floatIntensity={0}> {/* disable react-three/drei's internal animation */}
      <group scale={[scale, scale, scale]}>
        <RoundedBox args={[3, 2, 0.1]} radius={0.1} smoothness={4}>
          <meshStandardMaterial color="#1e1e2e" roughness={0.3} metalness={0.2} />
        </RoundedBox>
        <Text
          position={[0, 0, 0.1]}
          fontSize={0.4}
          color="#cdd6f4"
          anchorX="center"
          anchorY="middle"
        >
          Hello 3D
        </Text>
      </group>
    </Float>
  );
};
```

## Combining 3D with 2D Overlays

Layer 3D canvas with 2D React elements using `<AbsoluteFill>`:

```tsx
export const HybridScene: React.FC = () => {
  const { width, height } = useVideoConfig();
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* 3D layer */}
      <ThreeCanvas width={width} height={height}>
        <ambientLight intensity={0.5} />
        <RotatingCube />
      </ThreeCanvas>

      {/* 2D overlay on top */}
      <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 80 }}>
        <h1 style={{ color: '#fff', fontSize: 60, opacity: titleOpacity, margin: 0 }}>
          3D + React
        </h1>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

## Complete Working Example

```tsx
import React from 'react';
import { ThreeCanvas } from '@remotion/three';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

const OrbitingSpheres: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const angle = interpolate(frame, [0, 180], [0, Math.PI * 2]);
  const entryScale = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });

  const colors = ['#6366f1', '#f59e0b', '#10b981'];
  const radius = 2.5;

  return (
    <group scale={[entryScale, entryScale, entryScale]}>
      {colors.map((color, i) => {
        const offset = (i / colors.length) * Math.PI * 2;
        const x = Math.cos(angle + offset) * radius;
        const z = Math.sin(angle + offset) * radius;

        return (
          <mesh key={i} position={[x, 0, z]}>
            <sphereGeometry args={[0.4, 32, 32]} />
            <meshStandardMaterial color={color} roughness={0.2} metalness={0.8} />
          </mesh>
        );
      })}
      {/* Center sphere */}
      <mesh>
        <sphereGeometry args={[0.8, 32, 32]} />
        <meshStandardMaterial color="#18181b" roughness={0.1} metalness={0.9} />
      </mesh>
    </group>
  );
};

export const ThreeDScene: React.FC = () => {
  const { width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#09090b' }}>
      <ThreeCanvas width={width} height={height}>
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={2} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#6366f1" />
        <perspectiveCamera makeDefault position={[0, 3, 8]} fov={45} />
        <OrbitingSpheres />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
```
