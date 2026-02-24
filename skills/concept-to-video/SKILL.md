---
name: concept-to-video
description: >
  Turn any concept into an animated explainer video using Manim (Python). Use whenever the user
  wants animated visualizations, motion graphics, or video output (MP4/GIF) for technical concepts.
  Covers: architecture animations, data flow visualizations, algorithm step-throughs, pipeline
  explainers, math proofs, comparisons, agent interactions, training loops, or any "animate X" /
  "make a video of X" request. Also trigger for existing Manim scene edits or re-renders.
  Trigger on: "create a video", "animate this", "make an explainer", "concept to video",
  "manim animation", "show this as a video", "motion graphic", "visualize this process",
  or any concept + video/animation output request. Use this skill even for casual "animate"
  requests about technical ideas.
metadata:
  version: 1.0.0
---

# Concept to Video

Creates animated explainer videos from concepts using Manim (Python) as a programmatic animation engine.

## Reference Files

| File                            | Purpose                                                                    |
| ------------------------------- | -------------------------------------------------------------------------- |
| `references/scene-patterns.md`  | Common scene patterns for different concept types with reusable templates  |
| `scripts/render_video.py`       | Wrapper around Manim CLI — handles quality, format, output path cleanup    |

## Why Manim as the engine

Manim is the "SVG of video" — you write Python code that describes animations declaratively, and it renders to MP4/GIF at any resolution. The Python scene file IS the editable intermediate: the user can see the code, request changes ("make the arrows red", "add a third step", "slow down the transition"), and only do a final high-quality render once satisfied. This makes the workflow iterative and controllable, exactly like concept-to-image uses HTML as an intermediate.

## Workflow

```
Concept → Manim scene (.py) → Preview (low-quality) → Iterate → Final render (MP4/GIF)
```

1. **Interpret** the user's concept — determine the best animation approach
2. **Design** a self-contained Manim scene file — one file, one Scene class
3. **Preview** by rendering at low quality (`-ql`) for fast iteration
4. **Iterate** on the scene based on user feedback
5. **Export** final video at high quality using `scripts/render_video.py`

## Step 0: Ensure dependencies

Before writing any scene, ensure Manim is installed:

```bash
# System deps (usually pre-installed)
apt-get install -y libpango1.0-dev libcairo2-dev ffmpeg 2>/dev/null

# Python package
pip install manim --break-system-packages -q
```

Verify with: `python3 -c "import manim; print(manim.__version__)"`

## Step 1: Interpret the concept

Determine the best animation pattern. Read `references/scene-patterns.md` for detailed templates.

| User intent                     | Animation pattern            | Key Manim primitives                          |
| ------------------------------- | ---------------------------- | --------------------------------------------- |
| Explain a pipeline/flow         | Sequential flow animation    | Arrow, Rectangle, Text, AnimationGroup        |
| Show architecture layers        | Layer build-up               | VGroup, Arrange, FadeIn with shift            |
| Algorithm step-through          | State machine transitions    | Transform, ReplacementTransform, Indicate     |
| Compare approaches              | Side-by-side morph           | Split screen VGroups, simultaneous animations |
| Data transformation             | Object metamorphosis         | Transform chains, color transitions           |
| Mathematical concept            | Equation + geometric proof   | MathTex, geometric shapes, Rotate, Scale      |
| Agent/multi-system interaction  | Message passing animation    | Arrows between entities, Create/FadeOut       |
| Training/optimization loop      | Iterative cycle animation    | Loop with Transform, ValueTracker, plots      |
| Timeline/history                | Left-to-right progression    | NumberLine, sequential Indicate                |

## Step 2: Design the Manim scene

Core rules:

- **Single file, single Scene class**: Everything in one `.py` file with one `class XxxScene(Scene)`.
- **Self-contained**: No external assets unless absolutely necessary. Use Manim primitives for everything.
- **Readable code**: The scene file IS the user's artifact. Use clear variable names, comments for each animation beat.
- **Color with intention**: Use Manim's color constants (BLUE, RED, GREEN, YELLOW, etc.) or hex colors. Max 4-5 colors. Every color should encode meaning.
- **Pacing**: Include `self.wait()` calls between logical sections. 0.5s for breathing room, 1-2s for major transitions.
- **Text legibility**: Use `font_size=36` minimum for body text, `font_size=48+` for titles. Test at target resolution.
- **Scene dimensions**: Default Manim canvas is 14.2 × 8 units (16:9). Keep content within ±6 horizontal, ±3.5 vertical.

### Animation best practices

```python
# DO: Use animation groups for simultaneous effects
self.play(FadeIn(box), Write(label), run_time=1)

# DO: Use .animate syntax for property changes
self.play(box.animate.shift(RIGHT * 2).set_color(GREEN))

# DO: Stagger related elements
self.play(LaggedStart(*[FadeIn(item) for item in items], lag_ratio=0.2))

# DON'T: Add/remove without animation (jarring)
self.add(box)  # Only for setup before first frame

# DON'T: Make animations too fast
self.play(Transform(a, b), run_time=0.3)  # Too fast to read
```

### Structure template

```python
from manim import *

class ConceptScene(Scene):
    def construct(self):
        # === Section 1: Title / Setup ===
        title = Text("Concept Name", font_size=56, weight=BOLD)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # === Section 2: Core animation ===
        # ... main content here ...

        # === Section 3: Summary / Conclusion ===
        # ... wrap-up animation ...
        self.wait(2)
```

## Step 3: Preview render

Use low quality for fast iteration:

```bash
python3 scripts/render_video.py scene.py ConceptScene --quality low --format mp4
```

This renders at 480p/15fps — fast enough for previewing timing and layout. Present the video to the user.

## Step 4: Iterate

Common refinement requests and how to handle them:

| Request                    | Action                                                  |
| -------------------------- | ------------------------------------------------------- |
| "Slower/faster"            | Adjust `run_time=` params and `self.wait()` durations   |
| "Change colors"            | Update color constants                                  |
| "Add a step"               | Insert new animation block between sections             |
| "Reorder"                  | Move code blocks around                                 |
| "Different layout"         | Adjust `.shift()`, `.next_to()`, `.arrange()` calls     |
| "Add labels/annotations"   | Add `Text` or `MathTex` objects with `.next_to()`       |
| "Make it loop"             | Add matching intro/outro states                         |

## Step 5: Final export

Once the user is satisfied:

```bash
python3 scripts/render_video.py scene.py ConceptScene --quality high --format mp4
```

### Quality presets

| Preset   | Resolution | FPS | Flag  | Use case             |
| -------- | ---------- | --- | ----- | -------------------- |
| `low`    | 480p       | 15  | `-ql` | Fast preview         |
| `medium` | 720p       | 30  | `-qm` | Draft review         |
| `high`   | 1080p      | 60  | `-qh` | Final delivery       |
| `4k`     | 2160p      | 60  | `-qk` | Presentation quality |

### Format options

| Format | Flag            | Use case                        |
| ------ | --------------- | ------------------------------- |
| `mp4`  | `--format mp4`  | Standard video delivery         |
| `gif`  | `--format gif`  | Embeddable in docs, social      |
| `webm` | `--format webm` | Web-optimized                   |

### Delivering the output

Present both:
1. The `.py` scene file (for future editing)
2. The rendered video file (final output)

Copy the final video to `/mnt/user-data/outputs/` and present it.

## Error Handling

| Error                          | Cause                                      | Resolution                                                |
| ------------------------------ | ------------------------------------------ | --------------------------------------------------------- |
| `ModuleNotFoundError: manim`   | Manim not installed                        | Run Step 0 setup commands                                 |
| `pangocairo` build error       | Missing system dev headers                 | `apt-get install -y libpango1.0-dev`                      |
| `FileNotFoundError: ffmpeg`    | ffmpeg not installed                       | `apt-get install -y ffmpeg`                               |
| Scene class not found          | Class name mismatch                        | Verify class name matches CLI argument                    |
| Overlapping objects            | Positions not calculated                   | Use `.next_to()`, `.arrange()`, explicit `.shift()` calls |
| Text cut off                   | Text too large or positioned near edge     | Reduce `font_size` or adjust position within ±6,±3.5      |
| Slow render                    | Too many objects or complex transformations | Reduce object count, simplify paths, use lower quality    |
| `LaTeX Error`                  | LaTeX not installed (for MathTex)          | Use `Text` instead, or install `texlive-latex-base`       |

### LaTeX fallback

If LaTeX is not available, avoid `MathTex` and `Tex`. Use `Text` with Unicode math symbols instead:

```python
# Instead of: MathTex(r"\frac{1}{n} \sum_{i=1}^{n} x_i")
# Use:        Text("(1/n) Σ xᵢ", font_size=36)
```

## Limitations

- **Manim + ffmpeg required** — cannot render without these dependencies.
- **No audio support in this workflow** — Manim supports audio but adds complexity. Keep videos silent or add audio post-export.
- **LaTeX optional** — MathTex requires a LaTeX installation. Fall back to Text with Unicode for math.
- **Render time scales with complexity** — a 30-second 1080p scene with many objects can take 1-2 minutes to render.
- **3D scenes require OpenGL** — ThreeDScene may not work in headless containers. Stick to 2D Scene class.
- **No interactivity** — output is a static video file, not an interactive widget.

## Design anti-patterns to avoid

- Walls of text on screen — keep to 3-5 words per label, max 2 lines
- Everything appearing at once — use staged animations with LaggedStart
- Uniform timing — vary run_time to create rhythm (fast for simple, slow for important)
- No visual hierarchy — use size, color, and position to guide attention
- Rainbow colors — 3-4 intentional colors max
- Ignoring the grid — align objects to consistent positions using arrange/align
