"""
test_coniunctio.py - Comprehensive Test Suite for Coniunctio Engine Persistence & v0.6 Adaptation
"""

import os
import math
from coniunctio_v06 import AdaptiveConiunctioEngine

def test_v06_adaptive_threshold_breathing():
    # Initialize engine with baseline threshold of 2.0
    engine = AdaptiveConiunctioEngine(threshold=2.0, adapt_rate=1.0, homeostatic_drift=0.05)
    initial_threshold = engine.ground.threshold
    
    # Force a sustained high-tension load profile that triggers FRICTION phase streaks
    engine.dyad.set_tension(5.0, 5.0)
    
    # Run multiple steps to build up the friction streak (> 2 steps)
    for _ in range(5):
        engine.step()
        
    # Verify threshold expanded under sustained load
    assert engine.ground.threshold > initial_threshold, "Threshold should expand under sustained high friction load."
    
    # Now restore balanced/low tension to trigger homeostatic recovery
    engine.dyad.set_tension(0.1, -0.1)
    expanded_threshold = engine.ground.threshold
    
    # Run integration steps
    for _ in range(10):
        engine.step()
        
    # Verify threshold drifts back toward baseline
    assert engine.ground.threshold < expanded_threshold, "Threshold should drift homeostatically back toward baseline during stable integration."
    print("v0.6 Adaptive Threshold Breathing test passed successfully!")

def test_engine_basic_step():
    engine = AdaptiveConiunctioEngine(threshold=2.0)
    engine.dyad.set_tension(0.5, -0.5)
    engine.step()
    assert engine.witness.observation_count == 1
    assert engine.current_phase in {"GROUND", "INTEGRATION", "FRICTION"}
    print("Basic engine step test passed successfully!")

if __name__ == "__main__":
    print("Running Coniunctio Engine Test Suite...")
    test_v06_adaptive_threshold_breathing()
    test_engine_basic_step()
    print("All tests passed successfully!")
