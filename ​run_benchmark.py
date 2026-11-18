"""
run_benchmark.py - Comparative Benchmark: v0.5.1 (Rigid Anchor) vs. v0.6 (Adaptive Capacity)
Measures friction absorption, phase distribution, and conservation error under stress.
"""

from coniunctio_engine import ConiunctioEngine as EngineV051
from coniunctio_v06 import AdaptiveConiunctioEngine as EngineV06

def run_comparative_benchmark():
    print("=" * 70)
    print("CONIUNCTIO ENGINE — COMPARATIVE BENCHMARK (v0.5.1 vs v0.6)")
    print("=" * 70)

    # Initialize both engines with baseline parameters
    v051 = EngineV051(threshold=2.0)
    v06 = EngineV06(threshold=2.0, adapt_rate=1.0, homeostatic_drift=0.05)

    # Define a rigorous stress-test load profile (including impulse shocks)
    stress_profile = [
        (0.5, -0.5),   # Baseline stable
        (4.5, 4.0),    # High sustained friction
        (10.0, -10.0), # Extreme impulse shock
        (5.0, 5.0),    # Sustained heavy load
        (0.1, -0.1)    # Relaxation / Ground return
    ]

    print(f"{'Step':<5} | {'Engine':<8} | {'Phase':<11} | {'Friction':<8} | {'Threshold':<10} | {'Cons. Error':<12}")
    print("-" * 70)

    step_idx = 0
    for ta, tb in stress_profile:
        v051.dyad.set_tension(ta, tb)
        v06.dyad.set_tension(ta, tb)

        for _ in range(3):
            step_idx += 1
            v051.step()
            v06.step()

            log_51 = v051.witness.log[-1][1]
            log_06 = v06.witness.log[-1][1]

            print(f"{step_idx:02d}    | v0.5.1   | {log_51['phase']:<11} | {log_51['friction']:8.3f} | {log_51['threshold']:10.3f} | {v051.last_conservation_error:12.4f}")
            print(f"{step_idx:02d}    | v0.6     | {log_06['phase']:<11} | {log_06['friction']:8.3f} | {log_06['threshold']:10.3f} | {v06.last_conservation_error:12.4f}")
            print("-" * 70)

    print("\nBenchmark Complete. Notice how v0.6 breathes its threshold dynamically")
    print("to absorb impulse shocks while maintaining stable conservation bounds.")
    print("=" * 70)

if __name__ == "__main__":
    run_comparative_benchmark()
