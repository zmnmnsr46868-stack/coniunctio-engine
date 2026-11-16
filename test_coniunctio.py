"""
Test Suite for Coniunctio Engine: Evolutionary Loop Simulation
Simulates multiple cycles of cognitive and emotional input to observe 
when coherence drops into noise versus when it achieves phase lock.
"""

from coniunctio_engine import ConiunctioEngine, MagneticDyad

def run_simulation():
    engine = ConiunctioEngine()
    
    # A sequence of states representing varying degrees of internal friction and noise
    test_stream = [
        (0.8, 0.9, 0.7),  # High tension / heavy noise
        (0.4, 0.3, 0.2),  # Moderate tension
        (0.1, 0.1, 0.05), # Approaching stillness / high coherence
        (0.0, 0.0, 0.0),  # Pure baseline at [0, 0, 0]
        (0.5, 0.6, 0.4)   # Re-entering active dynamics
    ]
    
    print("=== STARTING CONIUNCTIO SIMULATION LOOP ===")
    for thought, feeling, instinct in test_stream:
        engine.step(thought, feeling, instinct)
    print("=== SIMULATION COMPLETE: BASELINE SECURED ===")

if __name__ == "__main__":
    run_simulation()
