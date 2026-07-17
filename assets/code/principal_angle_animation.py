"""Render the principal-angle mechanism used in the random-projection post.

From the repository root:

    manim -qm assets/code/principal_angle_animation.py PrincipalAngleMechanism

The scene is silent and deliberately paced. Each shot answers one question,
introduces only one implication, and keeps all labels inside a 16:9 safe area.
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
    Ellipse,
    FadeIn,
    FadeOut,
    Flash,
    GrowArrow,
    GrowFromCenter,
    LEFT,
    Line,
    MathTex,
    NumberLine,
    PI,
    Rectangle,
    RIGHT,
    Scene,
    Text,
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
GRID = "#A9B5C5"
SPHERE_FILL = "#E8F5F5"
BACKGROUND = "#FDFDFD"

config.background_color = BACKGROUND


class PrincipalAngleMechanism(Scene):
    """Follow one spectral value to the global incompatibility bound."""

    def step_heading(self, number: str, title: str) -> VGroup:
        step = Text(
            f"STEP {number} OF 4",
            font_size=21,
            weight="SEMIBOLD",
            color=ACCENT,
        )
        label = Text(title, font_size=32, weight="SEMIBOLD", color=INK)
        return VGroup(step, label).arrange(RIGHT, buff=0.35).move_to(UP * 3.2)

    def construct(self) -> None:
        self.show_question()
        self.show_spectral_block()
        self.show_principal_angle()
        self.show_bloch_angle()
        self.show_threshold()
        self.show_summary()

    def show_question(self) -> None:
        question = Text(
            "How can a large random pair be maximally incompatible?",
            font_size=38,
            weight="SEMIBOLD",
            color=INK,
        ).move_to(UP * 1.45)
        answer = Text(
            "One two-dimensional block can force the answer.",
            font_size=31,
            weight="SEMIBOLD",
            color=ACCENT,
        ).move_to(UP * 0.25)
        rule = Text(
            "Any parent measurement on the full space must also work on each reducing block.",
            font_size=25,
            color=MUTED,
        ).move_to(DOWN * 0.65)
        route = VGroup(
            MathTex(
                r"\lambda\approx\tfrac12",
                r"\Longrightarrow",
                r"\theta\approx\tfrac\pi4",
                color=INK,
            ),
            MathTex(
                r"(\sigma_z,\sigma_x)",
                r"\Longrightarrow",
                r"\tau\to\tfrac1{\sqrt2}",
                color=INK,
            ),
        ).arrange(DOWN, buff=0.35).scale(0.95).move_to(DOWN * 1.8)

        self.play(FadeIn(question, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(answer), run_time=0.65)
        self.play(FadeIn(rule), run_time=0.65)
        self.play(Write(route), run_time=1.1)
        self.wait(2.6)
        self.play(FadeOut(VGroup(question, answer, rule, route)), run_time=0.6)

    def show_spectral_block(self) -> None:
        heading = self.step_heading("1", "Locate one critical spectral value")
        axis = NumberLine(
            x_range=[0, 1, 0.25],
            length=9.4,
            include_numbers=False,
            color=GRID,
            stroke_width=4,
            tip_shape=None,
        ).move_to(UP * 0.9)
        zero = MathTex("0", color=MUTED).scale(0.8).next_to(axis.n2p(0), DOWN, buff=0.2)
        one = MathTex("1", color=MUTED).scale(0.8).next_to(axis.n2p(1), DOWN, buff=0.2)

        left_value, right_value = 0.22, 0.78
        interval = Line(axis.n2p(left_value), axis.n2p(right_value), color=ACCENT, stroke_width=12)
        left_cap = Line(UP * 0.2, DOWN * 0.2, color=ACCENT, stroke_width=4).move_to(axis.n2p(left_value))
        right_cap = left_cap.copy().move_to(axis.n2p(right_value))
        left_label = MathTex(r"\lambda^-", color=INK).next_to(left_cap, UP, buff=0.2)
        right_label = MathTex(r"\lambda^+", color=INK).next_to(right_cap, UP, buff=0.2)

        half_line = Line(UP * 0.62, DOWN * 0.62, color=MARKER, stroke_width=4).move_to(axis.n2p(0.5))
        half_dot = Dot(axis.n2p(0.5), radius=0.11, color=MARKER)
        half_label = MathTex(r"\tfrac12", color=MARKER).next_to(half_line, DOWN, buff=0.18)

        block_box = Rectangle(
            width=3.5,
            height=1.25,
            color=ACCENT,
            stroke_width=3,
            fill_color=SPHERE_FILL,
            fill_opacity=1,
        ).move_to(RIGHT * 2.35 + DOWN * 1.15)
        block_text = VGroup(
            Text("one 2D reducing block", font_size=24, weight="SEMIBOLD", color=INK),
            MathTex(r"\lambda\approx\tfrac12", color=MARKER).scale(0.95),
        ).arrange(DOWN, buff=0.18).move_to(block_box)
        block_arrow = Arrow(
            axis.n2p(0.5) + DOWN * 0.12,
            block_box.get_top() + LEFT * 0.55,
            buff=0.12,
            color=MARKER,
            stroke_width=4,
        )
        conclusion = Text(
            "If 1/2 lies in the limiting interval, such blocks occur arbitrarily closely.",
            font_size=25,
            color=MUTED,
        ).move_to(DOWN * 2.25)

        self.play(FadeIn(heading, shift=DOWN * 0.08), run_time=0.5)
        self.play(Create(axis), FadeIn(zero), FadeIn(one), run_time=0.8)
        self.play(
            Create(interval),
            Create(left_cap),
            Create(right_cap),
            FadeIn(left_label),
            FadeIn(right_label),
            run_time=0.9,
        )
        self.play(Create(half_line), GrowFromCenter(half_dot), FadeIn(half_label), run_time=0.8)
        self.play(Flash(half_dot, color=MARKER, flash_radius=0.38), run_time=0.65)
        self.play(GrowArrow(block_arrow), DrawBorderThenFill(block_box), FadeIn(block_text), run_time=1.0)
        self.play(FadeIn(conclusion, shift=UP * 0.06), run_time=0.55)
        self.wait(3.0)
        self.play(
            FadeOut(
                VGroup(
                    heading,
                    axis,
                    zero,
                    one,
                    interval,
                    left_cap,
                    right_cap,
                    left_label,
                    right_label,
                    half_line,
                    half_dot,
                    half_label,
                    block_arrow,
                    block_box,
                    block_text,
                    conclusion,
                )
            ),
            run_time=0.65,
        )

    def show_principal_angle(self) -> None:
        heading = self.step_heading("2", "Translate that value into a principal angle")
        origin = LEFT * 2.65 + DOWN * 0.05
        e_line = Line(LEFT * 2.25, RIGHT * 2.25, color=INK, stroke_width=5).move_to(origin)
        e_label = MathTex("E", color=INK).next_to(e_line.get_right(), DOWN, buff=0.12)
        theta = ValueTracker(0.16)

        f_line = always_redraw(
            lambda: Line(
                origin + 2.15 * np.array([-np.cos(theta.get_value()), -np.sin(theta.get_value()), 0]),
                origin + 2.15 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                color=ACCENT,
                stroke_width=6,
            )
        )
        angle_arc = always_redraw(
            lambda: Arc(
                radius=0.78,
                start_angle=0,
                angle=theta.get_value(),
                arc_center=origin,
                color=MARKER,
                stroke_width=5,
            )
        )
        f_label = always_redraw(
            lambda: MathTex("F", color=ACCENT).next_to(f_line.get_right(), UP, buff=0.12)
        )

        equations = VGroup(
            MathTex(r"\lambda=\cos^2\theta", color=INK),
            MathTex(r"\lambda\approx\tfrac12", color=MARKER),
            MathTex(r"\theta\approx\tfrac\pi4=45^\circ", color=INK),
        ).arrange(DOWN, buff=0.5).scale(1.05).move_to(RIGHT * 3.05)
        exact_angle = MathTex(r"\theta\approx45^\circ", color=MARKER).scale(0.78)
        exact_angle.move_to(origin + np.array([1.22, 0.72, 0]))
        conclusion = Text(
            "The spectral value selects a 45° principal-angle block.",
            font_size=26,
            color=MUTED,
        ).move_to(DOWN * 2.25)

        self.play(FadeIn(heading, shift=DOWN * 0.08), run_time=0.5)
        self.play(Create(e_line), FadeIn(e_label), Create(f_line), FadeIn(f_label), run_time=0.85)
        self.add(angle_arc)
        self.play(Write(equations[0]), run_time=0.75)
        self.play(Write(equations[1]), run_time=0.65)
        self.play(theta.animate.set_value(PI / 4), run_time=2.0, rate_func=rate_functions.ease_in_out_cubic)
        self.play(Write(equations[2]), FadeIn(exact_angle), run_time=0.85)
        self.play(Flash(exact_angle, color=MARKER, flash_radius=0.5), FadeIn(conclusion), run_time=0.7)
        self.wait(3.0)
        self.play(
            FadeOut(VGroup(heading, e_line, e_label, f_line, f_label, angle_arc, exact_angle, equations, conclusion)),
            run_time=0.65,
        )

    def bloch_sphere(self) -> VGroup:
        center = LEFT * 2.75 + DOWN * 0.1
        sphere = Circle(
            radius=1.72,
            color=GRID,
            stroke_width=4,
            fill_color=SPHERE_FILL,
            fill_opacity=1,
        ).move_to(center)
        equator = Ellipse(width=3.44, height=0.92, color=GRID, stroke_width=4).move_to(center)
        meridian = Ellipse(width=1.0, height=3.44, color=GRID, stroke_width=2).move_to(center)
        center_dot = Dot(center, radius=0.065, color=INK)
        z_arrow = Arrow(
            center,
            center + UP * 1.48,
            buff=0,
            color=ACCENT,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.18,
        )
        x_arrow = Arrow(
            center,
            center + RIGHT * 1.48,
            buff=0,
            color=MARKER,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.18,
        )
        z_label = MathTex(r"\sigma_z", color=ACCENT).scale(0.9).next_to(z_arrow.get_end(), RIGHT, buff=0.1)
        x_label = MathTex(r"\sigma_x", color=MARKER).scale(0.9).next_to(x_arrow.get_end(), UP, buff=0.1)
        right_angle = Arc(
            radius=0.68,
            start_angle=0,
            angle=PI / 2,
            arc_center=center,
            color=INK,
            stroke_width=3,
        )
        angle_label = MathTex(r"2\theta\approx\tfrac\pi2", color=INK).scale(0.78)
        angle_label.move_to(center + np.array([0.95, 0.88, 0]))
        return VGroup(
            sphere,
            equator,
            meridian,
            center_dot,
            z_arrow,
            x_arrow,
            z_label,
            x_label,
            right_angle,
            angle_label,
        )

    def show_bloch_angle(self) -> None:
        heading = self.step_heading("3", "Centering the projections doubles the angle")
        bloch = self.bloch_sphere()
        sphere, equator, meridian, center_dot = bloch[0:4]
        z_arrow, x_arrow, z_label, x_label, right_angle, angle_label = bloch[4:]

        bridge = MathTex(r"P\longmapsto D=2P-I", color=INK).scale(1.0)
        bridge.move_to(RIGHT * 3.0 + UP * 1.25)
        equations = VGroup(
            MathTex(r"D_E=\sigma_z", color=ACCENT),
            MathTex(r"D_F=\sigma_x", color=MARKER),
            MathTex(r"\angle(D_E,D_F)=2\theta\approx\tfrac\pi2", color=INK),
        ).arrange(DOWN, buff=0.48).scale(0.98).move_to(RIGHT * 3.0 + DOWN * 0.15)
        conclusion = Text(
            "The 45° subspace angle becomes two perpendicular Bloch directions.",
            font_size=25,
            color=MUTED,
        ).move_to(DOWN * 2.35)

        self.play(FadeIn(heading, shift=DOWN * 0.08), run_time=0.5)
        self.play(DrawBorderThenFill(sphere), Create(equator), Create(meridian), FadeIn(center_dot), run_time=1.0)
        self.play(Write(bridge), run_time=0.75)
        self.play(GrowArrow(z_arrow), FadeIn(z_label), Write(equations[0]), run_time=0.85)
        self.play(GrowArrow(x_arrow), FadeIn(x_label), Write(equations[1]), run_time=0.85)
        self.play(Create(right_angle), FadeIn(angle_label), Write(equations[2]), run_time=0.85)
        self.play(FadeIn(conclusion, shift=UP * 0.06), run_time=0.55)
        self.wait(3.2)

        self.stage_three_heading = heading
        self.stage_three_bridge = bridge
        self.stage_three_equations = equations
        self.stage_three_conclusion = conclusion
        self.bloch = bloch

    def show_threshold(self) -> None:
        heading = self.step_heading("4", "Use the Pauli pair to compute the threshold")
        self.play(
            FadeOut(self.stage_three_heading),
            FadeOut(self.stage_three_bridge),
            FadeOut(self.stage_three_equations),
            FadeOut(self.stage_three_conclusion),
            FadeIn(heading, shift=DOWN * 0.08),
            run_time=0.65,
        )

        norms = MathTex(r"\|z+x\|=\|z-x\|=\sqrt2", color=INK).scale(1.0)
        fraction = MathTex(r"\tau=\frac{2}{\sqrt2+\sqrt2}", color=INK).scale(1.05)
        answer = MathTex(r"\tau=\frac1{\sqrt2}", color=ACCENT).scale(1.28)
        calculation = VGroup(norms, fraction, answer).arrange(DOWN, buff=0.5)
        calculation.move_to(RIGHT * 3.0 + DOWN * 0.05)
        conclusion = Text(
            "the universal minimum for a binary pair",
            font_size=25,
            weight="SEMIBOLD",
            color=ACCENT,
        ).next_to(answer, DOWN, buff=0.38)

        self.play(Write(norms), run_time=0.85)
        self.play(Write(fraction), run_time=1.0)
        self.play(Write(answer), run_time=0.75)
        self.play(Flash(answer, color=ACCENT, flash_radius=0.72), FadeIn(conclusion), run_time=0.75)
        self.wait(3.4)
        self.play(FadeOut(VGroup(heading, self.bloch, calculation, conclusion)), run_time=0.7)

    def show_summary(self) -> None:
        heading = Text(
            "Why this local block controls the global pair",
            font_size=36,
            weight="SEMIBOLD",
            color=INK,
        ).move_to(UP * 2.65)
        row_one = MathTex(
            r"\tfrac12\in[\lambda^-,\lambda^+]",
            r"\Longrightarrow",
            r"\lambda\approx\tfrac12",
            r"\Longrightarrow",
            r"\theta\approx\tfrac\pi4",
            color=INK,
        ).scale(0.92).move_to(UP * 0.9)
        row_two = MathTex(
            r"D=2P-I",
            r"\Longrightarrow",
            r"(\sigma_z,\sigma_x)",
            r"\Longrightarrow",
            r"\tau\to\tfrac1{\sqrt2}",
            color=INK,
        ).scale(0.98).move_to(DOWN * 0.35)
        rule = Text(
            "A parent measurement for the full pair must restrict to this block.\n"
            "Therefore one Pauli-like block fixes the global upper bound.",
            font_size=26,
            color=MUTED,
            line_spacing=1.2,
        ).move_to(DOWN * 1.85)

        self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.65)
        self.play(Write(row_one), run_time=1.25)
        self.wait(0.8)
        self.play(Write(row_two), run_time=1.15)
        self.play(FadeIn(rule), run_time=0.65)
        self.wait(4.2)
        self.play(FadeOut(VGroup(heading, row_one, row_two, rule)), run_time=0.65)
