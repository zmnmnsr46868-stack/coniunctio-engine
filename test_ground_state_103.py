# test_ground_state_103.py
"""Unit tests for the THE 103 calibration model (ground_state_103.py)."""

from __future__ import annotations

import pytest

from ground_state_103 import GroundState103Model, TriadVector


def test_initial_ground_state() -> None:
    model = GroundState103Model()

    assert model.ground_coords == (0, 0, 0)
    assert model.state == TriadVector(0.0, 0.0, 0.0)
    assert model.state.gradient_magnitude() == 0.0
    assert model.state.plus_synthesis() == 0.0
    assert model.armor_weight == 0.0
    assert model.seam_visible is True
    assert model.spiral_turn == 0
    assert len(model.history) == 1
    assert model.history[0].action == "init_ground_state"


def test_apply_gradient_and_armor_clamping() -> None:
    model = GroundState103Model()
    model.apply_gradient(
        d_thought=0.6,
        d_memory=0.8,
        d_instinct=0.0,
        armor_delta=0.5,
        note="First gradient",
    )

    assert model.state.as_tuple() == (0.6, 0.8, 0.0)
    assert model.state.gradient_magnitude() == pytest.approx(1.0)
    assert model.armor_weight == 0.5
    assert model.spiral_turn == 1

    # Armor cannot drop below zero.
    model.apply_gradient(armor_delta=-2.0)
    assert model.armor_weight == 0.0
    assert model.spiral_turn == 2


def test_step_spiral_damping_and_validation() -> None:
    model = GroundState103Model()
    model.apply_gradient(d_thought=1.0, d_memory=1.0, d_instinct=1.0, armor_delta=1.0)

    plus_val = model.step_spiral(damping=0.5)
    assert plus_val == pytest.approx(0.5)
    assert model.state.as_tuple() == (0.5, 0.5, 0.5)
    assert model.armor_weight == pytest.approx(0.5)
    assert model.spiral_turn == 2

    with pytest.raises(ValueError):
        model.step_spiral(damping=1.5)

    with pytest.raises(ValueError):
        model.step_spiral(damping=-0.1)


def test_seam_obscuration_and_coherence() -> None:
    model = GroundState103Model()
    model.apply_gradient(d_thought=0.5, d_memory=0.5, d_instinct=0.5, armor_delta=0.8)
    visible_coherence = model.informational_coherence()

    model.seam_visible = False
    hidden_coherence = model.informational_coherence()

    assert hidden_coherence < visible_coherence


def test_reset_to_ground_restores_baseline() -> None:
    model = GroundState103Model()
    model.apply_gradient(d_thought=1.2, d_memory=0.9, d_instinct=0.7, armor_delta=2.0)
    model.seam_visible = False
    model.step_spiral(damping=0.8)

    model.reset_to_ground(restore_seam=True, note="Return to [0, 0, 0]")

    assert model.state == TriadVector(0.0, 0.0, 0.0)
    assert model.state.gradient_magnitude() == 0.0
    assert model.armor_weight == 0.0
    assert model.seam_visible is True
    assert model.spiral_turn == 3
    assert model.history[-1].action == "reset_to_ground"
    assert model.snapshot()["gradient_norm"] == 0.0
