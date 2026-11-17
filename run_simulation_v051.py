"""
run_simulation_v051.py - Extended test suite for v0.5.1
Tests Balanced, Asymmetric A, Asymmetric B, and Reinforcing profiles.
"""
from coniunctio_engine import ConiunctioEngine

def run_experiment(label, a, b, steps=25):
    print(f"\n{'=' * 72}")
    print(f"EXPERIMENT: {label} | Initial Tensions: A={a}, B={b}")
    print(f"{'=' * 72}")
    
    engine = ConiunctioEngine(threshold=2.0, adapt_rate=1.0, alpha=1.0, beta=0.1)
    engine.dyad.set_tension(a, b)
    
    for step in range(1, steps + 1):
        snapshot = engine.step()
        record = engine.witness.ledger[-1]
        print(
            f"Step {step:02d} | {record['from_phase']:<11} -> {record['to_phase']:<11} | "
            f"Fric: {snapshot['active_friction']:5.2f} | "
            f"Tens: {snapshot['total_tension']:5.2f} | "
            f"Net: {snapshot['net_force']:+6.2f} | "
            f"Eps_T: {snapshot['conservation_error']:.2e} | "
            f"Poles: ({snapshot['tension_a']:+5.2f}, {snapshot['tension_b']:+5.2f})"
        )

if __name__ == "__main__":
    run_experiment("Balanced", 5.0, -5.0, steps=10)
    run_experiment("Asymmetric A", 8.0, -2.0, steps=12)
    run_experiment("Reinforcing", 8.0, 2.0, steps=10)
