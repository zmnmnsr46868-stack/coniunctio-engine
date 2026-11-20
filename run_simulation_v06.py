"""
run_simulation_v06.py - Live simulation runner for Coniunctio Engine v0.6 ("Adaptive Capacity")
Observes homeostatic threshold breathing under varying tension load profiles.
"""

import json
from coniunctio_v06 import AdaptiveConiunctioEngine


def run_adaptive_simulation():
    print("=" * 60)
    print("CONIUNCTIO ENGINE v0.6 — ADAPTIVE CAPACITY SIMULATION")
    print("Core Seed: THE 88 | The pause is the geometry.")
    print("=" * 60)

    # Initialize engine with baseline threshold = 2.0 and homeostatic drift = 0.05
    engine = AdaptiveConiunctioEngine(
        threshold=2.0,
        adapt_rate=1.0,
        alpha=1.0,
        beta=0.1,
        homeostatic_drift=0.05,
    )

    # Define a sequence of load regimes (Tension A, Tension B) across steps
    load_profile = [
        (0.5, -0.5),  # Phase 1: Mild, balanced ground state
        (4.5, 4.0),   # Phase 2: Heavy symmetrical load (triggers FRICTION streak)
        (5.0, 5.0),   # Phase 3: Sustained heavy load (forces threshold expansion)
        (0.2, -0.2),  # Phase 4: Release / Return to integration (triggers homeostatic recovery)
        (0.1, -0.1),  # Phase 5: Deep stabilization back toward baseline
    ]

    history = []
    step_counter = 0

    for regime_idx, (ta, tb) in enumerate(load_profile, start=1):
        print(f"\n--- Load Regime {regime_idx}: Setting Tensions (A: {ta}, B: {tb}) ---")
        engine.dyad.set_tension(ta, tb)

        # Run 4 steps per regime to observe dynamics
        for sub_step in range(4):
            step_counter += 1
            engine.step()
            latest = engine.witness.log[-1][1]

            print(
                f" [Step {step_counter:02d}] Phase: {latest['phase']:<11} | "
                f"Friction: {latest['friction']:6.3f} | "
                f"Threshold: {latest['threshold']:6.3f} | "
                f"Streak: {latest['streak']} | "
                f"Conservation Err: {engine.last_conservation_error:.4f}"
            )

            # Map v0.6 engine metrics to analyzer.py trajectory schema
            raw_coherence = latest.get("coherence", 1.0 / (1.0 + latest["friction"]))
            coherence = max(0.0, min(1.0, float(raw_coherence)))
            state = "SPIRAL" if latest["phase"] in ("FRICTION", "SPIRAL") else latest["phase"]

            history.append({
                "cycle": step_counter,
                "state": state,
                "coherence": coherence,
                "spiral_depth": latest.get("spiral_depth", latest["streak"]),
                "tension": latest.get("tension", max(abs(ta), abs(tb))),
                "input": latest.get("input", [ta, tb, round(ta - tb, 4)]),
            })

    print("\n" + "=" * 60)
    print(f"Simulation Complete. Total Observations Witnessed: {engine.witness.observation_count}")
    print(f"Final Ground Threshold State: {engine.ground.threshold:.4f} (Base: {engine.base_threshold})")
    print("=" * 60)

    with open("trajectory_v06.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print("Exported trajectory data to trajectory_v06.json")


if __name__ == "__main__":
    run_adaptive_simulation()
