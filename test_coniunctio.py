"""
test_coniunctio.py - Comprehensive Test Suite for Coniunctio Engine Persistence & v0.6 Adaptation
"""

import math
from coniunctio_v06 import AdaptiveConiunctioEngine


def test_v06_adaptive_threshold_breathing():
    # Initialize engine with baseline threshold of 2.0
    engine = AdaptiveConiunctioEngine(
        threshold=2.0, adapt_rate=1.0, homeostatic_drift=0.05
    )
    initial_threshold = engine.ground.threshold

    # Force a sustained high-tension load profile that triggers FRICTION phase streaks
    engine.dyad.set_tension(5.0, 5.0)

    # Run multiple steps to build up the friction streak (> 2 steps)
    for _ in range(5):
        engine.step()

    # Verify threshold expanded under sustained load
    assert (
        engine.ground.threshold > initial_threshold
    ), "Threshold should expand under sustained high friction load."

    # Now restore balanced/low tension to trigger homeostatic recovery
    engine.dyad.set_tension(0.1, -0.1)
    expanded_threshold = engine.ground.threshold

    # Run integration steps
    for _ in range(10):
        engine.step()

    # Verify threshold drifts back toward baseline
    assert (
        engine.ground.threshold < expanded_threshold
    ), "Threshold should drift homeostatically back toward baseline during stable integration."
    print("v0.6 Adaptive Threshold Breathing test passed successfully!")


def test_engine_basic_step():
    engine = AdaptiveConiunctioEngine(threshold=2.0)
    engine.dyad.set_tension(0.5, -0.5)
    engine.step()
    assert engine.witness.observation_count == 1
    assert engine.current_phase in {"GROUND", "INTEGRATION", "FRICTION"}
    print("Basic engine step test passed successfully!")


def test_reversed_polarity_damping():
    # Reversed asymmetry: negative tension_a, positive tension_b
    engine = AdaptiveConiunctioEngine(threshold=2.0, adapt_rate=1.0)
    engine.dyad.set_tension(-8.0, 2.0)

    for _ in range(15):
        engine.step()

    assert engine.ground.is_stable(), "Engine should stabilize under reversed polarity."
    assert engine.dyad.tension_a <= 0.0, "Negative pole should damp toward 0 without crossing sign."
    assert engine.dyad.tension_b >= 0.0, "Positive pole should damp toward 0 without crossing sign."
    print("Reversed polarity damping test passed successfully!")


def test_reinforcing_polarity_damping():
    # Reinforcing asymmetry: both poles positive
    engine = AdaptiveConiunctioEngine(threshold=2.0, adapt_rate=1.0)
    engine.dyad.set_tension(8.0, 2.0)

    for _ in range(20):
        engine.step()

    assert engine.ground.is_stable(), "Engine should stabilize under reinforcing polarity."
    assert math.isclose(
        engine.dyad.tension_a, engine.dyad.tension_b, abs_tol=1e-9
    ), "Reinforcing poles should equalize during integration."
    print("Reinforcing polarity damping test passed successfully!")


def test_energy_conservation_in_integration():
    engine = AdaptiveConiunctioEngine(threshold=2.0)
    engine.dyad.set_tension(1.2, -0.8)  # Initial total tension = 2.0, net_force = 0.4 -> stable
    initial_energy = engine.dyad.get_total_tension()

    for _ in range(5):
        engine.step()
        assert engine.current_phase == "INTEGRATION"
        assert (
            engine.last_conservation_error < 1e-9
        ), f"Conservation error too high: {engine.last_conservation_error}"

    assert math.isclose(
        engine.dyad.get_total_tension(), initial_energy, rel_tol=1e-9
    ), "Total tension energy must be conserved across integration steps."
    print("Energy conservation test passed successfully!")


def test_non_finite_input_rejection():
    engine = AdaptiveConiunctioEngine(threshold=2.0)
    for bad_val in (float("nan"), float("inf"), float("-inf")):
        try:
            engine.dyad.set_tension(bad_val, 1.0)
            assert False, f"Expected ValueError for {bad_val}"
        except ValueError:
            pass
    print("Non-finite input rejection test passed successfully!")


if __name__ == "__main__":
    print("Running Coniunctio Engine Test Suite...")
    test_v06_adaptive_threshold_breathing()
    test_engine_basic_step()
    test_reversed_polarity_damping()
    test_reinforcing_polarity_damping()
    test_energy_conservation_in_integration()
    test_non_finite_input_rejection()
    print("All tests passed!")
