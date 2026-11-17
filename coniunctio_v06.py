"""
coniunctio_v06.py - Coniunctio Engine v0.6 ("Adaptive Capacity")
Extends core dynamics with homeostatic threshold breathing and dynamic adaptation rates.
"""

class Witness:
    def __init__(self):
        self.observation_count = 0
        self.log = []

    def record(self, state_snapshot: dict):
        self.observation_count += 1
        self.log.append((self.observation_count, state_snapshot))


class MagneticDyad:
    def __init__(self, tension_a: float = 0.0, tension_b: float = 0.0):
        self.tension_a = tension_a
        self.tension_b = tension_b

    def set_tension(self, a: float, b: float):
        self.tension_a = a
        self.tension_b = b

    def get_net_force(self) -> float:
        return self.tension_a + self.tension_b

    def get_total_tension(self) -> float:
        return abs(self.tension_a) + abs(self.tension_b)


class GroundState:
    def __init__(self, threshold: float = 2.0):
        self.base_threshold = threshold
        self.threshold = threshold
        self.friction = 0.0
        self.peak_friction = 0.0

    def compute_friction(self, net_force: float, total_tension: float, alpha: float, beta: float) -> float:
        self.friction = (alpha * abs(net_force)) + (beta * total_tension)
        if self.friction > self.peak_friction:
            self.peak_friction = self.friction
        return self.friction

    def is_stable(self) -> bool:
        return self.friction <= self.threshold


class AdaptiveConiunctioEngine:
    def __init__(self, threshold: float = 2.0, adapt_rate: float = 1.0, alpha: float = 1.0, beta: float = 0.1, homeostatic_drift: float = 0.05):
        self.base_threshold = threshold
        self.threshold = threshold
        self.adapt_rate = adapt_rate
        self.alpha = alpha
        self.beta = beta
        self.homeostatic_drift = homeostatic_drift
        
        self.dyad = MagneticDyad(0.0, 0.0)
        self.ground = GroundState(threshold=threshold)
        self.witness = Witness()
        
        self.current_phase = "GROUND"
        self.last_conservation_error = 0.0
        self.friction_step_streak = 0

    def step(self):
        net_force = self.dyad.get_net_force()
        total_tension = self.dyad.get_total_tension()
        
        friction = self.ground.compute_friction(net_force, total_tension, self.alpha, self.beta)
        
        if self.ground.is_stable():
            self.current_phase = "INTEGRATION"
            self.friction_step_streak = 0
            
            # Homeostatic recovery: drift threshold back toward base configuration
            if self.ground.threshold > self.base_threshold:
                self.ground.threshold = max(self.base_threshold, self.ground.threshold - self.homeostatic_drift)
                self.threshold = self.ground.threshold

            pre_energy = total_tension
            self.dyad.tension_a *= 0.95
            self.dyad.tension_b *= 1.05
            post_energy = self.dyad.get_total_tension()
            self.last_conservation_error = abs(pre_energy - post_energy)
        else:
            self.current_phase = "FRICTION"
            self.friction_step_streak += 1
            
            # Adaptive Capacity: Expand threshold dynamically under sustained high load
            if self.friction_step_streak > 2:
                expansion = self.homeostatic_drift * (friction / self.ground.threshold)
                self.ground.threshold += expansion
                self.threshold = self.ground.threshold

            reduction = (self.adapt_rate + (0.1 * self.friction_step_streak)) * (friction - self.ground.threshold)
            if self.dyad.tension_a > 0:
                self.dyad.tension_a = max(0.0, self.dyad.tension_a - reduction / 2)
            if self.dyad.tension_b < 0:
                self.dyad.tension_b = min(0.0, self.dyad.tension_b + reduction / 2)

        self.witness.record({
            "phase": self.current_phase,
            "friction": friction,
            "threshold": self.ground.threshold,
            "streak": self.friction_step_streak,
            "t_a": self.dyad.tension_a,
            "t_b": self.dyad.tension_b
        })
