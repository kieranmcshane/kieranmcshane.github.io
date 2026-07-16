"""Render the principal-angle mechanism used in the random-projection post.

From the repository root:

    manim -qm assets/code/principal_angle_animation.py PrincipalAngleMechanism

The scene is intentionally silent. Its on-screen text and the prose beneath the
embedded video provide the complete explanation without audio.
"""

from __future__ import annotations

import numpy as np

from manim import (
    Arc,
    Arrow,
    Circle,
    Create,
    Dot,
    DOWN,
    DrawBorderThenFill,
    FadeIn,
    FadeOut,
    Flash,
    GrowArrow,
    GrowFromCenter,
    LEFT,
    Line,
    MathTex,
    NumberLine,
    ORIGIN,
    PI,
    RIGHT,
    Scene,
    Text,
    TransformMatchingTex,
    UP,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    config,
    rate_functions,
)


INK = "#172033"
MUTED = "#5D6778"
ACCENT = "#087F8C"
MARKER = "#A33B20"
GRID = "#C8D0DB"
BACKGROUND = "#FDFDFD"

config.background_color = BACKGROUND


class PrincipalAngleMechanism(Scene):
    """Animate the spectral interval, critical block, and Pauli obstruction."""

    def section_heading(self, step: str, title: str) -> VGroup:
        badge = Text(step, font_size=26, weight="SEMIBOLD", color=ACCENT)
        label = Text(title, font_size=34, weight="SEMIBOLD", color=INK)
        return VGroup(badge, label).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.48)

    def construct(self) -> None:
        title = Text(
            "Why does the phase disk reach maximal incompatibility?",
            font_size=42,
            weight="SEMIBOLD",
            color=INK,
        )
        subtitle = Text(
            "Follow one critical principal-angle block",
            font_size=27,
            color=MUTED,
        ).next_to(title, DOWN, buff=0.32)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.12), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.6)

        self.show_spectral_interval()
        self.show_principal_angle()
        self.show_pauli_block()
        self.show_compatibility_threshold()

    def show_spectral_interval(self) -> None:
        heading = self.section_heading("1", "The limiting interval reaches one half")
        self.play(FadeIn(heading, shift=DOWN * 0.12), run_time=0.6)

        axis = NumberLine(
            x_range=[0, 1, 0.25],
            length=9.2,
            include_numbers=False,
            color=GRID,
            stroke_width=4,
            tip_shape=None,
        ).shift(DOWN * 0.15)
        zero = MathTex("0", color=MUTED).scale(0.8).next_to(axis.n2p(0), DOWN, buff=0.22)
        one = MathTex("1", color=MUTED).scale(0.8).next_to(axis.n2p(1), DOWN, buff=0.22)

        left_value, right_value = 0.22, 0.78
        interval = Line(
            axis.n2p(left_value),
            axis.n2p(right_value),
            color=ACCENT,
            stroke_width=12,
        )
        left_cap = Line(UP * 0.19, DOWN * 0.19, color=ACCENT, stroke_width=4).move_to(
            axis.n2p(left_value)
        )
        right_cap = left_cap.copy().move_to(axis.n2p(right_value))
        left_label = MathTex(r"\lambda^-", color=INK).next_to(left_cap, UP, buff=0.22)
        right_label = MathTex(r"\lambda^+", color=INK).next_to(right_cap, UP, buff=0.22)

        half_line = Line(UP * 0.72, DOWN * 0.72, color=MARKER, stroke_width=4).move_to(
            axis.n2p(0.5)
        )
        half_dot = Dot(axis.n2p(0.5), radius=0.105, color=MARKER)
        half_label = MathTex(r"\tfrac12", color=MARKER).next_to(half_line, DOWN, buff=0.2)
        conclusion = MathTex(
            r"\tfrac12\in[\lambda^-,\lambda^+]",
            color=INK,
        ).scale(1.2).to_edge(DOWN, buff=0.72)

        self.play(Create(axis), FadeIn(zero), FadeIn(one), run_time=0.8)
        self.play(
            Create(interval),
            Create(left_cap),
            Create(right_cap),
            FadeIn(left_label),
            FadeIn(right_label),
            run_time=1.0,
        )
        self.play(Create(half_line), GrowFromCenter(half_dot), FadeIn(half_label), run_time=0.8)
        self.play(Flash(half_dot, color=MARKER, flash_radius=0.35), Write(conclusion), run_time=0.9)
        self.wait(0.9)

        self.play(
            FadeOut(VGroup(axis, zero, one, interval, left_cap, right_cap, left_label, right_label)),
            FadeOut(heading),
            FadeOut(half_line),
            FadeOut(half_label),
            half_dot.animate.move_to(ORIGIN),
            conclusion.animate.move_to(UP * 1.9),
            run_time=0.8,
        )

        critical_value = MathTex(r"\cos^2\theta=\tfrac12", color=INK).scale(1.2)
        critical_value.move_to(conclusion)
        self.play(TransformMatchingTex(conclusion, critical_value), FadeOut(half_dot), run_time=0.9)
        self.wait(0.4)

        self.critical_value = critical_value

    def show_principal_angle(self) -> None:
        heading = self.section_heading("2", "A critical two-dimensional block")
        self.play(FadeIn(heading, shift=DOWN * 0.12), run_time=0.5)

        origin = DOWN * 0.55
        e_line = Line(LEFT * 4.5, RIGHT * 4.5, color=INK, stroke_width=5).move_to(origin)
        e_label = MathTex("E", color=INK).next_to(e_line.get_right(), UP, buff=0.12)
        theta = ValueTracker(0.18)

        f_line = always_redraw(
            lambda: Line(
                origin + 4.0 * np.array([-np.cos(theta.get_value()), -np.sin(theta.get_value()), 0]),
                origin + 4.0 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                color=ACCENT,
                stroke_width=6,
            )
        )
        angle_arc = always_redraw(
            lambda: Arc(
                radius=1.05,
                start_angle=0,
                angle=theta.get_value(),
                arc_center=origin,
                color=MARKER,
                stroke_width=5,
            )
        )
        theta_label = always_redraw(
            lambda: MathTex(
                rf"\theta={theta.get_value() / PI:.2f}\pi",
                color=MARKER,
            )
            .scale(0.8)
            .move_to(origin + np.array([1.65, 0.68, 0]))
        )
        f_label = always_redraw(
            lambda: MathTex("F", color=ACCENT).next_to(f_line.get_right(), UP, buff=0.12)
        )

        self.play(Create(e_line), FadeIn(e_label), Create(f_line), run_time=0.8)
        self.add(angle_arc, theta_label, f_label)
        self.play(
            theta.animate.set_value(PI / 4),
            run_time=2.2,
            rate_func=rate_functions.ease_in_out_cubic,
        )

        exact_angle = MathTex(r"\theta=\tfrac\pi4", color=MARKER).scale(1.0)
        exact_angle.move_to(origin + np.array([1.78, 0.82, 0]))
        self.remove(theta_label)
        self.add(exact_angle)
        self.play(Flash(exact_angle, color=MARKER, flash_radius=0.55), run_time=0.7)
        self.wait(0.7)

        self.play(
            FadeOut(VGroup(heading, self.critical_value, e_line, e_label, exact_angle)),
            FadeOut(f_line),
            FadeOut(angle_arc),
            FadeOut(f_label),
            run_time=0.7,
        )

    def show_pauli_block(self) -> None:
        heading = self.section_heading("3", "Center the two projections")
        self.play(FadeIn(heading, shift=DOWN * 0.12), run_time=0.5)

        projections = MathTex(
            r"P_E=\begin{pmatrix}1&0\\0&0\end{pmatrix}",
            r"\qquad",
            r"P_F=\tfrac12\begin{pmatrix}1&1\\1&1\end{pmatrix}",
            color=INK,
        ).scale(1.0).shift(UP * 0.55)
        center_rule = MathTex(r"D=2P-I", color=MUTED).scale(0.95).next_to(
            projections, DOWN, buff=0.65
        )

        self.play(Write(projections), run_time=1.5)
        self.play(FadeIn(center_rule, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        paulis = MathTex(
            r"D_E=\sigma_z",
            r"\qquad",
            r"D_F=\sigma_x",
            color=INK,
        ).scale(1.35)
        self.play(
            TransformMatchingTex(projections, paulis),
            FadeOut(center_rule),
            run_time=1.4,
        )

        perpendicular = Text(
            "The critical block becomes two perpendicular Bloch directions",
            font_size=27,
            color=MUTED,
        ).next_to(paulis, DOWN, buff=0.65)
        self.play(FadeIn(perpendicular, shift=UP * 0.1), run_time=0.6)
        self.wait(0.8)

        self.play(FadeOut(VGroup(heading, paulis, perpendicular)), run_time=0.7)

    def show_compatibility_threshold(self) -> None:
        heading = self.section_heading("4", "The Pauli obstruction fixes the threshold")
        self.play(FadeIn(heading, shift=DOWN * 0.12), run_time=0.5)

        sphere = Circle(radius=1.65, color=GRID, stroke_width=4).shift(LEFT * 2.7 + DOWN * 0.15)
        equator = Arc(
            radius=1.65,
            start_angle=0,
            angle=PI,
            color=GRID,
            stroke_width=3,
        ).stretch(0.32, 1).move_to(sphere)
        center = Dot(sphere.get_center(), radius=0.07, color=INK)
        z_arrow = Arrow(
            sphere.get_center(),
            sphere.get_center() + UP * 1.45,
            buff=0,
            color=ACCENT,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.18,
        )
        x_arrow = Arrow(
            sphere.get_center(),
            sphere.get_center() + RIGHT * 1.45,
            buff=0,
            color=MARKER,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.18,
        )
        z_label = MathTex(r"\sigma_z", color=ACCENT).next_to(z_arrow.get_end(), RIGHT, buff=0.12)
        x_label = MathTex(r"\sigma_x", color=MARKER).next_to(x_arrow.get_end(), UP, buff=0.12)

        formula = MathTex(
            r"\tau",
            r"=\frac{2}{\|z+x\|+\|z-x\|}",
            r"=\frac1{\sqrt2}",
            color=INK,
        ).scale(1.12).shift(RIGHT * 2.35 + UP * 0.35)
        result = Text(
            "universal binary minimum",
            font_size=27,
            weight="SEMIBOLD",
            color=ACCENT,
        ).next_to(formula, DOWN, buff=0.5)

        self.play(DrawBorderThenFill(sphere), Create(equator), FadeIn(center), run_time=1.0)
        self.play(GrowArrow(z_arrow), FadeIn(z_label), run_time=0.7)
        self.play(GrowArrow(x_arrow), FadeIn(x_label), run_time=0.7)
        self.play(Write(formula[0:2]), run_time=1.1)
        self.play(Write(formula[2]), run_time=0.8)
        self.play(Flash(formula[2], color=ACCENT, flash_radius=0.65), FadeIn(result), run_time=0.8)
        self.wait(1.8)

        chain = MathTex(
            r"\tfrac12\in[\lambda^-,\lambda^+]",
            r"\Longrightarrow",
            r"\theta\approx\tfrac\pi4",
            r"\Longrightarrow",
            r"(\sigma_z,\sigma_x)",
            r"\Longrightarrow",
            r"\tau\to\tfrac1{\sqrt2}",
            color=INK,
        ).scale(0.82).to_edge(DOWN, buff=0.46)

        self.play(
            FadeOut(VGroup(heading, sphere, equator, center, z_arrow, x_arrow, z_label, x_label, formula, result)),
            run_time=0.6,
        )
        self.play(Write(chain), run_time=1.5)
        self.wait(1.8)
        self.play(FadeOut(chain), run_time=0.6)
