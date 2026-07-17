"""Render the principal-angle mechanism used in the random-projection post.

From the repository root:

    manim -qm assets/code/principal_angle_animation.py PrincipalAngleMechanism

The scene is intentionally silent. Each shot answers one question and keeps all
labels inside a generous 16:9 safe area.
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
GRID = "#B8C2D0"
SPHERE_FILL = "#E8F5F5"
BACKGROUND = "#FDFDFD"

config.background_color = BACKGROUND


class PrincipalAngleMechanism(Scene):
    """Follow one spectral value all the way to the Pauli obstruction."""

    def step_heading(self, number: str, title: str) -> VGroup:
        step = Text(number, font_size=25, weight="SEMIBOLD", color=ACCENT)
        label = Text(title, font_size=33, weight="SEMIBOLD", color=INK)
        return VGroup(step, label).arrange(RIGHT, buff=0.32).move_to(UP * 3.25)

    def construct(self) -> None:
        self.show_purpose()
        self.show_spectral_value()
        self.show_principal_angle()
        self.show_bloch_angle()
        self.show_threshold()
        self.show_summary()

    def show_purpose(self) -> None:
        title = Text(
            "Why one qubit-sized block controls the whole pair",
            font_size=39,
            weight="SEMIBOLD",
            color=INK,
        ).move_to(UP * 1.15)
        subtitle = Text(
            "A joint measurement for the full pair must work on every reducing block.",
            font_size=27,
            color=MUTED,
        ).next_to(title, DOWN, buff=0.38)
        route = MathTex(
            r"\lambda=\tfrac12",
            r"\Longrightarrow",
            r"\theta=\tfrac\pi4",
            r"\Longrightarrow",
            r"(\sigma_z,\sigma_x)",
            r"\Longrightarrow",
            r"\tau=\tfrac1{\sqrt2}",
            color=INK,
        ).scale(0.87).move_to(DOWN * 0.65)

        self.play(FadeIn(title, shift=UP * 0.12), run_time=0.8)
        self.play(FadeIn(subtitle), Write(route), run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(VGroup(title, subtitle, route)), run_time=0.55)

    def show_spectral_value(self) -> None:
        heading = self.step_heading("1", "The spectral interval contains one half")
        axis = NumberLine(
            x_range=[0, 1, 0.25],
            length=9.4,
            include_numbers=False,
            color=GRID,
            stroke_width=4,
            tip_shape=None,
        ).move_to(UP * 0.35)
        zero = MathTex("0", color=MUTED).scale(0.78).next_to(axis.n2p(0), DOWN, buff=0.22)
        one = MathTex("1", color=MUTED).scale(0.78).next_to(axis.n2p(1), DOWN, buff=0.22)

        left_value, right_value = 0.22, 0.78
        interval = Line(axis.n2p(left_value), axis.n2p(right_value), color=ACCENT, stroke_width=12)
        left_cap = Line(UP * 0.2, DOWN * 0.2, color=ACCENT, stroke_width=4).move_to(
            axis.n2p(left_value)
        )
        right_cap = left_cap.copy().move_to(axis.n2p(right_value))
        left_label = MathTex(r"\lambda^-", color=INK).next_to(left_cap, UP, buff=0.22)
        right_label = MathTex(r"\lambda^+", color=INK).next_to(right_cap, UP, buff=0.22)

        half_line = Line(UP * 0.68, DOWN * 0.68, color=MARKER, stroke_width=4).move_to(
            axis.n2p(0.5)
        )
        half_dot = Dot(axis.n2p(0.5), radius=0.105, color=MARKER)
        half_label = MathTex(r"\tfrac12", color=MARKER).next_to(half_line, DOWN, buff=0.2)
        condition = MathTex(r"\tfrac12\in[\lambda^-,\lambda^+]", color=INK).scale(1.18)
        condition.move_to(DOWN * 1.38)
        meaning = Text(
            "So the random pair contains blocks with a spectral value approaching 1/2.",
            font_size=25,
            color=MUTED,
        ).move_to(DOWN * 2.3)

        self.play(FadeIn(heading, shift=DOWN * 0.1), run_time=0.45)
        self.play(Create(axis), FadeIn(zero), FadeIn(one), run_time=0.65)
        self.play(
            Create(interval),
            Create(left_cap),
            Create(right_cap),
            FadeIn(left_label),
            FadeIn(right_label),
            run_time=0.85,
        )
        self.play(Create(half_line), GrowFromCenter(half_dot), FadeIn(half_label), run_time=0.65)
        self.play(Flash(half_dot, color=MARKER, flash_radius=0.35), Write(condition), run_time=0.75)
        self.play(FadeIn(meaning, shift=UP * 0.08), run_time=0.45)
        self.wait(0.8)

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
                    condition,
                    meaning,
                )
            ),
            run_time=0.55,
        )

    def show_principal_angle(self) -> None:
        heading = self.step_heading("2", "Convert the spectral value into an angle")
        origin = LEFT * 2.55 + DOWN * 0.25
        e_line = Line(LEFT * 2.4, RIGHT * 2.4, color=INK, stroke_width=5).move_to(origin)
        e_label = MathTex("E", color=INK).next_to(e_line.get_right(), UP, buff=0.12)
        theta = ValueTracker(0.20)

        f_line = always_redraw(
            lambda: Line(
                origin + 2.25 * np.array([-np.cos(theta.get_value()), -np.sin(theta.get_value()), 0]),
                origin + 2.25 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
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
            lambda: MathTex("F", color=ACCENT).next_to(f_line.get_right(), UP, buff=0.1)
        )

        equations = VGroup(
            MathTex(r"\lambda=\cos^2\theta", color=INK),
            MathTex(r"\lambda=\tfrac12", color=MARKER),
            MathTex(r"\theta=\tfrac\pi4", color=INK),
        ).arrange(DOWN, buff=0.43).scale(1.08).move_to(RIGHT * 3.25 + UP * 0.15)
        note = Text(
            "The two projection subspaces meet at 45°.",
            font_size=25,
            color=MUTED,
        ).move_to(DOWN * 2.35)

        self.play(FadeIn(heading, shift=DOWN * 0.1), run_time=0.45)
        self.play(Create(e_line), FadeIn(e_label), Create(f_line), FadeIn(f_label), run_time=0.7)
        self.add(angle_arc)
        self.play(Write(equations[0]), run_time=0.55)
        self.play(Write(equations[1]), theta.animate.set_value(PI / 4), run_time=1.65, rate_func=rate_functions.ease_in_out_cubic)
        exact_angle = MathTex(r"\theta=\tfrac\pi4", color=MARKER).scale(0.85)
        exact_angle.move_to(origin + np.array([1.12, 0.68, 0]))
        self.play(Write(equations[2]), FadeIn(exact_angle), run_time=0.65)
        self.play(Flash(exact_angle, color=MARKER, flash_radius=0.5), FadeIn(note), run_time=0.65)
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(heading, e_line, e_label, f_line, f_label, angle_arc, exact_angle, equations, note)),
            run_time=0.55,
        )

    def bloch_sphere(self) -> VGroup:
        center = LEFT * 2.8 + DOWN * 0.15
        sphere = Circle(
            radius=1.75,
            color=GRID,
            stroke_width=4,
            fill_color=SPHERE_FILL,
            fill_opacity=1,
        ).move_to(center)
        equator = Ellipse(width=3.5, height=0.92, color=GRID, stroke_width=4).move_to(center)
        meridian = Ellipse(width=1.0, height=3.5, color=GRID, stroke_width=2).move_to(center)
        center_dot = Dot(center, radius=0.065, color=INK)
        z_arrow = Arrow(
            center,
            center + UP * 1.52,
            buff=0,
            color=ACCENT,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.18,
        )
        x_arrow = Arrow(
            center,
            center + RIGHT * 1.52,
            buff=0,
            color=MARKER,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.18,
        )
        z_label = MathTex(r"D_E=\sigma_z", color=ACCENT).scale(0.82)
        z_label.next_to(z_arrow.get_end(), RIGHT, buff=0.1)
        x_label = MathTex(r"D_F=\sigma_x", color=MARKER).scale(0.82)
        x_label.next_to(x_arrow.get_end(), UP, buff=0.1)
        right_angle = Arc(
            radius=0.72,
            start_angle=0,
            angle=PI / 2,
            arc_center=center,
            color=INK,
            stroke_width=3,
        )
        angle_label = MathTex(r"2\theta=\tfrac\pi2", color=INK).scale(0.75)
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

        center_rule = MathTex(r"D=2P-I", color=MUTED).scale(0.95)
        center_rule.move_to(RIGHT * 3.15 + UP * 1.35)
        paulis = VGroup(
            MathTex(r"D_E=2P_E-I=\sigma_z", color=INK),
            MathTex(r"D_F=2P_F-I=\sigma_x", color=INK),
            MathTex(r"\angle(D_E,D_F)=2\theta=\tfrac\pi2", color=MARKER),
        ).arrange(DOWN, buff=0.48).scale(0.92).move_to(RIGHT * 3.2 + DOWN * 0.15)
        note = Text(
            "A 45° principal angle becomes two perpendicular Bloch directions.",
            font_size=25,
            color=MUTED,
        ).move_to(DOWN * 2.45)

        self.play(FadeIn(heading, shift=DOWN * 0.1), run_time=0.45)
        self.play(DrawBorderThenFill(sphere), Create(equator), Create(meridian), FadeIn(center_dot), run_time=0.9)
        self.play(Write(center_rule), run_time=0.45)
        self.play(GrowArrow(z_arrow), FadeIn(z_label), Write(paulis[0]), run_time=0.7)
        self.play(GrowArrow(x_arrow), FadeIn(x_label), Write(paulis[1]), run_time=0.7)
        self.play(Create(right_angle), FadeIn(angle_label), Write(paulis[2]), run_time=0.7)
        self.play(FadeIn(note, shift=UP * 0.08), FadeOut(center_rule), run_time=0.5)
        self.wait(0.9)

        self.bloch = bloch
        self.bloch_heading = heading
        self.bloch_equations = paulis
        self.bloch_note = note

    def show_threshold(self) -> None:
        new_heading = self.step_heading("4", "The perpendicular pair fixes the threshold")
        self.play(
            FadeOut(self.bloch_heading),
            FadeOut(self.bloch_equations),
            FadeOut(self.bloch_note),
            FadeIn(new_heading, shift=DOWN * 0.1),
            run_time=0.55,
        )

        norms = MathTex(r"\|z+x\|=\|z-x\|=\sqrt2", color=INK).scale(1.0)
        norms.move_to(RIGHT * 3.1 + UP * 0.75)
        formula = MathTex(
            r"\tau",
            r"=\frac{2}{\|z+x\|+\|z-x\|}",
            r"=\frac1{\sqrt2}",
            color=INK,
        ).scale(0.96).move_to(RIGHT * 3.1 + DOWN * 0.45)
        result = Text(
            "the universal minimum for a binary pair",
            font_size=25,
            weight="SEMIBOLD",
            color=ACCENT,
        ).move_to(RIGHT * 3.1 + DOWN * 1.55)

        self.play(Write(norms), run_time=0.65)
        self.play(Write(formula[0:2]), run_time=0.9)
        self.play(Write(formula[2]), run_time=0.55)
        self.play(Flash(formula[2], color=ACCENT, flash_radius=0.62), FadeIn(result), run_time=0.65)
        self.wait(1.25)

        self.play(
            FadeOut(VGroup(new_heading, self.bloch, norms, formula, result)),
            run_time=0.6,
        )

    def show_summary(self) -> None:
        heading = Text(
            "One small block certifies the global obstruction",
            font_size=35,
            weight="SEMIBOLD",
            color=INK,
        ).move_to(UP * 2.5)
        row_one = MathTex(
            r"\tfrac12\in[\lambda^-,\lambda^+]",
            r"\Longrightarrow",
            r"\theta\approx\tfrac\pi4",
            r"\Longrightarrow",
            r"\angle(D_E,D_F)\approx\tfrac\pi2",
            color=INK,
        ).scale(0.88).move_to(UP * 0.55)
        row_two = MathTex(
            r"(D_E,D_F)\approx(\sigma_z,\sigma_x)",
            r"\Longrightarrow",
            r"\tau\to\tfrac1{\sqrt2}",
            color=INK,
        ).scale(1.0).move_to(DOWN * 0.75)
        note = Text(
            "A parent for the full measurements would restrict to this block.",
            font_size=25,
            color=MUTED,
        ).move_to(DOWN * 2.15)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.55)
        self.play(Write(row_one), run_time=1.05)
        self.play(Write(row_two), run_time=0.85)
        self.play(FadeIn(note), run_time=0.45)
        self.wait(1.6)
        self.play(FadeOut(VGroup(heading, row_one, row_two, note)), run_time=0.55)
