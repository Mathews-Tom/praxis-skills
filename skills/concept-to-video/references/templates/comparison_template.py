"""
Side-by-Side Comparison Template — parametric A vs B visualization.

Customize LEFT_SIDE, RIGHT_SIDE, and their items. Works for any two-option comparison.
Run with: manim -ql comparison_template.py ComparisonScene

Config:
    TITLE           — main title at top
    LEFT_LABEL      — label for left panel
    LEFT_COLOR      — accent color for left panel
    LEFT_ITEMS      — list of feature strings for left side
    RIGHT_LABEL     — label for right panel
    RIGHT_COLOR     — accent color for right panel
    RIGHT_ITEMS     — list of feature strings for right side
"""

from manim import *

# ── Config ─────────────────────────────────────────────────────────────────
TITLE = "Monolith vs Microservices"

LEFT_LABEL = "Monolith"
LEFT_COLOR = BLUE
LEFT_ITEMS = [
    "Single deployable unit",
    "Shared memory/state",
    "Simple local dev",
    "Harder to scale",
    "Single point of failure",
]

RIGHT_LABEL = "Microservices"
RIGHT_COLOR = GREEN
RIGHT_ITEMS = [
    "Independent deployments",
    "Isolated state per service",
    "Complex local dev",
    "Scale services independently",
    "Isolated failure domains",
]
# ───────────────────────────────────────────────────────────────────────────

PANEL_X = 3.2   # horizontal distance from center for each panel
PANEL_Y = -0.3  # vertical center for content


class ComparisonScene(Scene):
    def construct(self) -> None:
        # Title
        title = Text(TITLE, font_size=44, weight=BOLD)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        # Divider
        divider = Line(UP * 2.8, DOWN * 3.2, color=GREY, stroke_width=1)
        self.play(Create(divider))

        # Panel labels
        left_title = Text(LEFT_LABEL, font_size=34, color=LEFT_COLOR, weight=BOLD)
        left_title.move_to(LEFT * PANEL_X + UP * 2.2)

        right_title = Text(RIGHT_LABEL, font_size=34, color=RIGHT_COLOR, weight=BOLD)
        right_title.move_to(RIGHT * PANEL_X + UP * 2.2)

        self.play(Write(left_title), Write(right_title))

        # Left items
        left_group = VGroup(*[
            Text(f"• {item}", font_size=20, color=LEFT_COLOR)
            for item in LEFT_ITEMS
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        left_group.move_to(LEFT * PANEL_X + DOWN * 0.3)

        # Right items (rendered as separate boxes to convey independence)
        right_group = VGroup(*[
            VGroup(
                RoundedRectangle(width=2.8, height=0.55, corner_radius=0.08,
                                 color=RIGHT_COLOR, fill_opacity=0.1),
                Text(item, font_size=18, color=RIGHT_COLOR),
            )
            for item in RIGHT_ITEMS
        ])
        right_group.arrange(DOWN, buff=0.18)
        right_group.move_to(RIGHT * PANEL_X + DOWN * 0.3)

        # Animate both sides
        self.play(
            LaggedStart(*[FadeIn(item, shift=LEFT * 0.2) for item in left_group], lag_ratio=0.15),
            LaggedStart(*[FadeIn(item, scale=0.85) for item in right_group], lag_ratio=0.15),
        )

        self.wait(2)
