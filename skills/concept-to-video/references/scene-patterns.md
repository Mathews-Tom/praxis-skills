# Scene Patterns Reference

Reusable templates for common concept visualization types. Each pattern includes a minimal working example that can be adapted.

---

## Pattern 1: Pipeline / Data Flow

For: RAG pipelines, ETL processes, request flows, CI/CD stages.

```python
from manim import *

class PipelineScene(Scene):
    def construct(self):
        # Define stages
        stages = ["Ingest", "Embed", "Index", "Retrieve", "Generate"]
        colors = [BLUE, TEAL, GREEN, YELLOW, RED]

        boxes = VGroup()
        for i, (name, color) in enumerate(zip(stages, colors)):
            box = VGroup(
                RoundedRectangle(corner_radius=0.2, width=2, height=1, color=color, fill_opacity=0.2),
                Text(name, font_size=28, color=color)
            )
            boxes.add(box)

        boxes.arrange(RIGHT, buff=0.5)
        boxes.move_to(ORIGIN)

        # Animate stage by stage
        for i, box in enumerate(boxes):
            self.play(FadeIn(box, shift=UP * 0.3), run_time=0.5)
            if i < len(boxes) - 1:
                arrow = Arrow(
                    boxes[i].get_right(), boxes[i + 1].get_left(),
                    buff=0.1, color=WHITE, stroke_width=2
                )
                self.play(GrowArrow(arrow), run_time=0.3)

        self.wait(2)
```

---

## Pattern 2: Architecture Layers

For: System architecture, network stacks, abstraction layers.

```python
from manim import *

class ArchitectureScene(Scene):
    def construct(self):
        layers = [
            ("Application", BLUE),
            ("API Gateway", TEAL),
            ("Service Mesh", GREEN),
            ("Infrastructure", ORANGE),
        ]

        layer_group = VGroup()
        for name, color in layers:
            layer = VGroup(
                Rectangle(width=8, height=1.2, color=color, fill_opacity=0.15),
                Text(name, font_size=32, color=color)
            )
            layer_group.add(layer)

        layer_group.arrange(DOWN, buff=0.15)
        layer_group.move_to(ORIGIN)

        # Build from bottom up
        for layer in reversed(layer_group):
            self.play(FadeIn(layer, shift=UP * 0.5), run_time=0.6)

        # Add connecting arrows
        for i in range(len(layer_group) - 1):
            arrow = Arrow(
                layer_group[i].get_bottom(),
                layer_group[i + 1].get_top(),
                buff=0.05, color=GREY, stroke_width=2
            )
            self.play(GrowArrow(arrow), run_time=0.3)

        self.wait(2)
```

---

## Pattern 3: Algorithm Step-Through

For: Sorting, search, graph traversal, any stateful algorithm.

```python
from manim import *

class AlgorithmScene(Scene):
    def construct(self):
        title = Text("Binary Search", font_size=48, weight=BOLD)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        # Create array
        values = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        cells = VGroup()
        for v in values:
            cell = VGroup(
                Square(side_length=0.8, color=WHITE, stroke_width=1),
                Text(str(v), font_size=24)
            )
            cells.add(cell)

        cells.arrange(RIGHT, buff=0)
        cells.move_to(ORIGIN)
        self.play(FadeIn(cells))

        target_text = Text("Target: 23", font_size=32, color=YELLOW)
        target_text.next_to(cells, DOWN, buff=1)
        self.play(Write(target_text))

        # Simulate search steps
        lo, hi = 0, len(values) - 1
        target = 23

        while lo <= hi:
            mid = (lo + hi) // 2
            # Highlight search range
            highlight = SurroundingRectangle(
                VGroup(*cells[lo:hi + 1]),
                color=BLUE, buff=0.05
            )
            pointer = Arrow(
                cells[mid].get_top() + UP * 0.5,
                cells[mid].get_top(),
                buff=0.05, color=RED
            )
            mid_label = Text("mid", font_size=20, color=RED)
            mid_label.next_to(pointer, UP, buff=0.1)

            self.play(Create(highlight), GrowArrow(pointer), Write(mid_label), run_time=0.6)
            self.wait(0.5)

            if values[mid] == target:
                cells[mid][0].set_fill(GREEN, opacity=0.5)
                self.play(Indicate(cells[mid], color=GREEN, scale_factor=1.3))
                found = Text("Found!", font_size=40, color=GREEN)
                found.next_to(target_text, DOWN)
                self.play(Write(found))
                break
            elif values[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1

            self.play(FadeOut(highlight), FadeOut(pointer), FadeOut(mid_label), run_time=0.3)

        self.wait(2)
```

---

## Pattern 4: Side-by-Side Comparison

For: Before/after, two approaches, trade-off visualization.

```python
from manim import *

class ComparisonScene(Scene):
    def construct(self):
        title = Text("Monolith vs Microservices", font_size=44, weight=BOLD)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        divider = Line(UP * 2.5, DOWN * 2.5, color=GREY, stroke_width=1)
        self.play(Create(divider))

        # Left side: Monolith
        left_title = Text("Monolith", font_size=32, color=BLUE)
        left_title.move_to(LEFT * 3.5 + UP * 2)
        mono_box = Rectangle(width=3, height=4, color=BLUE, fill_opacity=0.1)
        mono_box.move_to(LEFT * 3.5 + DOWN * 0.5)
        mono_labels = VGroup(*[
            Text(s, font_size=18) for s in ["Auth", "API", "DB", "UI", "Logic"]
        ]).arrange(DOWN, buff=0.3).move_to(mono_box)

        # Right side: Microservices
        right_title = Text("Microservices", font_size=32, color=GREEN)
        right_title.move_to(RIGHT * 3.5 + UP * 2)
        micro_boxes = VGroup()
        for name, pos in [("Auth", UL), ("API", UR), ("DB", DL), ("UI", DR), ("Logic", DOWN)]:
            box = VGroup(
                RoundedRectangle(width=1.2, height=0.8, corner_radius=0.1,
                                 color=GREEN, fill_opacity=0.1),
                Text(name, font_size=16, color=GREEN)
            )
            micro_boxes.add(box)
        micro_boxes.arrange_in_grid(rows=2, cols=3, buff=0.3)
        micro_boxes.move_to(RIGHT * 3.5 + DOWN * 0.5)

        self.play(Write(left_title), Write(right_title))
        self.play(FadeIn(mono_box), FadeIn(mono_labels))
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in micro_boxes], lag_ratio=0.15))

        self.wait(2)
```

---

## Pattern 5: Message Passing / Agent Interaction

For: Multi-agent systems, distributed systems, pub/sub, request/response.

```python
from manim import *

class AgentInteractionScene(Scene):
    def construct(self):
        # Create agents
        agents = {}
        positions = {"Orchestrator": UP * 2, "Planner": LEFT * 4, "Executor": RIGHT * 4, "Memory": DOWN * 2}
        colors = {"Orchestrator": BLUE, "Planner": GREEN, "Executor": ORANGE, "Memory": PURPLE}

        for name, pos in positions.items():
            circle = Circle(radius=0.6, color=colors[name], fill_opacity=0.2)
            label = Text(name, font_size=20, color=colors[name])
            label.next_to(circle, DOWN, buff=0.15)
            agent = VGroup(circle, label).move_to(pos)
            agents[name] = agent

        all_agents = VGroup(*agents.values())
        self.play(LaggedStart(*[FadeIn(a, scale=0.5) for a in all_agents], lag_ratio=0.2))
        self.wait(0.5)

        # Animate message passing
        messages = [
            ("Orchestrator", "Planner", "Plan task", YELLOW),
            ("Planner", "Orchestrator", "Steps ready", GREEN),
            ("Orchestrator", "Executor", "Execute step 1", YELLOW),
            ("Executor", "Memory", "Store result", ORANGE),
            ("Executor", "Orchestrator", "Step complete", GREEN),
        ]

        for src, dst, msg_text, color in messages:
            src_pos = agents[src][0].get_center()
            dst_pos = agents[dst][0].get_center()

            msg = Text(msg_text, font_size=16, color=color)
            arrow = Arrow(src_pos, dst_pos, buff=0.7, color=color, stroke_width=2)
            msg.next_to(arrow, UP if src_pos[1] >= dst_pos[1] else DOWN, buff=0.1)

            self.play(GrowArrow(arrow), FadeIn(msg), run_time=0.6)
            self.play(Indicate(agents[dst][0], color=color), run_time=0.3)
            self.play(FadeOut(arrow), FadeOut(msg), run_time=0.3)

        self.wait(2)
```

---

## Pattern 6: Equation / Mathematical Concept

For: Loss functions, attention mechanisms, probability, any math.

Note: Uses `Text` with Unicode instead of `MathTex` to avoid LaTeX dependency.

```python
from manim import *

class MathConceptScene(Scene):
    def construct(self):
        title = Text("Attention Mechanism", font_size=48, weight=BOLD)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        # Show the formula using Text (LaTeX-free)
        formula = Text("Attention(Q, K, V) = softmax(QKᵀ / √dₖ) · V", font_size=30)
        formula.move_to(UP * 1)
        self.play(Write(formula), run_time=1.5)
        self.wait(1)

        # Break down components
        components = [
            ("Q = Query", "What am I looking for?", BLUE),
            ("K = Key", "What do I contain?", GREEN),
            ("V = Value", "What do I provide?", ORANGE),
        ]

        comp_group = VGroup()
        for symbol, desc, color in components:
            row = VGroup(
                Text(symbol, font_size=28, color=color),
                Text(f"→ {desc}", font_size=22, color=GREY),
            ).arrange(RIGHT, buff=0.5)
            comp_group.add(row)

        comp_group.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        comp_group.move_to(DOWN * 1.2)

        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in comp_group], lag_ratio=0.3))
        self.wait(2)
```

---

## Pattern 7: Iterative Process / Training Loop

For: Gradient descent, RL loops, feedback systems, any cyclic process.

```python
from manim import *

class TrainingLoopScene(Scene):
    def construct(self):
        title = Text("Training Loop", font_size=48, weight=BOLD)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP).scale(0.7))

        # Create cycle nodes
        steps = ["Forward\nPass", "Compute\nLoss", "Backward\nPass", "Update\nWeights"]
        colors = [BLUE, RED, ORANGE, GREEN]
        radius = 2.2
        n = len(steps)

        nodes = VGroup()
        for i, (step, color) in enumerate(zip(steps, colors)):
            angle = PI / 2 - i * TAU / n  # start from top, go clockwise
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            box = VGroup(
                RoundedRectangle(width=2, height=1, corner_radius=0.15,
                                 color=color, fill_opacity=0.15),
                Text(step, font_size=20, color=color)
            ).move_to(pos)
            nodes.add(box)

        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in nodes], lag_ratio=0.2))

        # Add arrows between nodes
        arrows = VGroup()
        for i in range(n):
            start = nodes[i].get_center()
            end = nodes[(i + 1) % n].get_center()
            direction = end - start
            arrow = Arrow(start, end, buff=0.85, color=GREY, stroke_width=2)
            arrows.add(arrow)
            self.play(GrowArrow(arrow), run_time=0.3)

        # Animate one "cycle" with a highlight traveling around
        for i in range(n):
            self.play(
                nodes[i][0].animate.set_fill(colors[i], opacity=0.5),
                run_time=0.4
            )
            self.play(
                nodes[i][0].animate.set_fill(colors[i], opacity=0.15),
                run_time=0.2
            )

        # Epoch counter
        epoch = Text("Epoch: 1 → 2 → 3 → ... → N", font_size=24, color=YELLOW)
        epoch.to_edge(DOWN)
        self.play(Write(epoch))
        self.wait(2)
```

---

## Utility Snippets

### Fade transition between sections

```python
# Clear everything and transition
self.play(*[FadeOut(mob) for mob in self.mobjects])
self.wait(0.3)
```

### Highlight / call attention

```python
# Flash a specific element
self.play(Indicate(element, color=YELLOW, scale_factor=1.2))

# Surround with box
box = SurroundingRectangle(element, color=RED, buff=0.15)
self.play(Create(box))
```

### Animated text replacement

```python
old_text = Text("Before", font_size=36)
new_text = Text("After", font_size=36, color=GREEN)
new_text.move_to(old_text)
self.play(ReplacementTransform(old_text, new_text))
```

### Progressive reveal with bullet points

```python
points = VGroup(*[
    Text(f"• {t}", font_size=24)
    for t in ["First point", "Second point", "Third point"]
]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
points.move_to(ORIGIN)

for point in points:
    self.play(FadeIn(point, shift=RIGHT * 0.3), run_time=0.5)
    self.wait(0.5)
```

### Screen wipe / scene transition

```python
# Slide everything left and bring new content from right
old_content = VGroup(*self.mobjects)
self.play(old_content.animate.shift(LEFT * 15), run_time=0.8)
self.remove(*old_content)
```
