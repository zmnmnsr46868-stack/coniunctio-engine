from coniunctio_engine import ConiunctioEngine, PHI_INV


def run_simulation():
    engine = ConiunctioEngine()

    # Stream: gentle entry -> sustained harmonic spiral -> sudden hijack spike -> recovery
    stream = [
        (0.20, 0.25, 0.15),  # Low friction: enters spiral
        (0.25, 0.30, 0.20),  # Prior adapts: spiral deepens
        (0.30, 0.35, 0.25),  # Sustained coherence
        (1.50, -1.20, 1.40), # Sudden hijack spike: triggers GroundState reset
        (0.10, 0.15, 0.10),  # Post-pause recovery back into spiral
    ]

    print("=== Coniunctio Engine v0.2 Simulation ===")
    for t, f, i in stream:
        rec = engine.step(t, f, i)
        print(
            f"Cycle {rec['cycle']} | State: {rec['state']:<12} | "
            f"Depth: {rec['spiral_depth']} | Coherence: {rec['coherence']:.4f} | "
            f"Prior: {rec['prior']}"
        )

    # Assertions for CI verification
    assert len(engine.history) == 5, "History should record all 5 cycles"
    assert engine.history[0]["state"] == "SPIRAL", "Cycle 1 should phase-lock"
    assert engine.history[2]["spiral_depth"] == 3, "Spiral depth should reach 3"
    assert engine.history[3]["state"] == "GROUND_RESET", "Hijack spike must trigger reset"
    assert engine.history[3]["prior"] == [0.0, 0.0, 0.0], "Reset must restore [0,0,0]"
    assert engine.history[4]["state"] == "SPIRAL", "Cycle 5 should re-enter spiral"
    assert round(PHI_INV, 3) == 0.618, "Golden ratio conjugate anchor check"

    print("\nAll v0.2 assertions passed successfully.")


if __name__ == "__main__":
    run_simulation()
