import math
import time

PHI_INV = (math.sqrt(5) - 1) / 2  # Golden ratio conjugate ≈ 0.61803398875
LEARNING_RATE = 1.0 - PHI_INV     # ≈ 0.38196601125 (predictive prior update weight)


class GroundState:
    """The unconditioned, unperturbed observer baseline at [0, 0, 0]."""
    def __init__(self):
        self.anchor = [0.0, 0.0, 0.0]

    def reset(self):
        return list(self.anchor)


class MagneticDyad:
    """Models active psychological polarities (Thought, Feeling, Instinct) against predictive priors."""
    def __init__(self, thought=0.0, feeling=0.0, instinct=0.0):
        self.vector = [float(thought), float(feeling), float(instinct)]

    def prediction_error(self, prior):
        """Calculates Euclidean magnitude of surprise (input minus expected prior)."""
        diff = [v - p for v, p in zip(self.vector, prior)]
        return math.sqrt(sum(d ** 2 for d in diff))


class Witness:
    """The central observer introducing the pause and measuring bounded coherence."""
    def __init__(self, threshold=PHI_INV):
        self.threshold = threshold

    def observe(self, tension):
        coherence = 1.0 / (1.0 + tension)
        phase_locked = coherence > self.threshold
        return coherence, phase_locked


class ConiunctioEngine:
    """Master v0.2 integration engine with stateful spiral memory and predictive priors."""
    def __init__(self):
        self.ground = GroundState()
        self.witness = Witness()
        self.prior = self.ground.reset()
        self.spiral_depth = 0
        self.history = []

    def step(self, thought, feeling, instinct):
        dyad = MagneticDyad(thought, feeling, instinct)
        tension = dyad.prediction_error(self.prior)
        coherence, locked = self.witness.observe(tension)

        if locked:
            self.spiral_depth += 1
            # Update predictive prior toward integrated state
            self.prior = [
                p + LEARNING_RATE * (v - p)
                for p, v in zip(self.prior, dyad.vector)
            ]
            state = "SPIRAL"
        else:
            # High surprise/noise: return to unconditioned GroundState anchor
            self.spiral_depth = 0
            self.prior = self.ground.reset()
            state = "GROUND_RESET"

        record = {
            "cycle": len(self.history) + 1,
            "input": dyad.vector,
            "tension": round(tension, 4),
            "coherence": round(coherence, 4),
            "state": state,
            "spiral_depth": self.spiral_depth,
            "prior": [round(x, 4) for x in self.prior],
            "timestamp": time.time(),
        }
        self.history.append(record)
        return record
