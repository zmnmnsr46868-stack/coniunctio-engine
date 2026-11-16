"""
Coniunctio Engine: Executable Consciousness Model
Models the interaction between the Witness @ [0,0,0] and the MagneticDyad 
to transform reactive loops into intentional evolutionary spirals.
"""

import math
import time

class GroundState:
    """Represents the unconditioned baseline at [0, 0, 0]."""
    def __init__(self):
        self.coordinates = (0.0, 0.0, 0.0)
        self.status = "Stable / Unperturbed"

    def measure(self):
        return self.coordinates

class MagneticDyad:
    """Models the active polarities: Thought, Feeling, and Instinct."""
    def __init__(self, thought=0.0, feeling=0.0, instinct=0.0):
        self.thought = thought
        self.feeling = feeling
        self.instinct = instinct

    def magnitude(self):
        return math.sqrt(self.thought**2 + self.feeling**2 + self.instinct**2)

class Witness:
    """The tuning fork / bounded function at the center."""
    def __init__(self):
        self.baseline = GroundState()

    def observe(self, dyad: MagneticDyad):
        tension = dyad.magnitude()
        # The pause introduces coherence
        coherence = 1.0 / (1.0 + tension)
        return coherence

class ConiunctioEngine:
    """The master integration loop."""
    def __init__(self):
        self.witness = Witness()
        self.current_spiral_cycle = 1

    def step(self, thought, feeling, instinct):
        dyad = MagneticDyad(thought, feeling, instinct)
        coherence = self.witness.observe(dyad)
        
        print(f"[CYCLE {self.current_spiral_cycle}] Tension: {dyad.magnitude():.3f} | Coherence: {coherence:.3f}")
        
        if coherence > 0.618:
            print(">> Phase Lock Achieved: Transitioning Loop to Spiral.")
        else:
            print(">> Noise detected. Maintaining baseline at [0, 0, 0].")
            
        self.current_spiral_cycle += 1
        return coherence

if __name__ == "__main__":
    engine = ConiunctioEngine()
    # Test simulation step
    engine.step(0.2, 0.3, 0.1)
