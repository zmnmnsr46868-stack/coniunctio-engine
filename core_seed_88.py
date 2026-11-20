from dataclasses import dataclass, field
from typing import Dict, List
import math

PHI_INV = (math.sqrt(5) - 1) / 2  # ≈ 0.618

@dataclass
class TriadState:
    thought: float
    feeling: float
    instinct: float
    note: str = ""

    @property
    def consciousness_tension(self) -> float:
        """
        Thought + Feeling + Instinct + Consciousness (the plus sign in the relation).
        Note: Instinct is divided by the Golden Ratio because it is the densest, 
        heaviest biological drag. It must be translated through the constant of harmony.
        """
        return round(self.thought + self.feeling + self.instinct / PHI_INV, 4)

    def cross_examine(self) -> Dict[str, str]:
        return {
            "thought_asks_feeling": f"How does this feel? (charge={self.feeling:.3f})",
            "feeling_asks_thought": f"What does this think? (charge={self.thought:.3f})",
            "instinct_asks_witness": f"What is the witness here? (charge={self.instinct:.3f} | {self.note})",
        }


@dataclass
class CoreSeed88:
    seed_id: int = 88
    setpoint: float = 0.618
    cycle: int = 0
    spiral_radius: float = 0.0
    archive: List[Dict[str, object]] = field(default_factory=list)
    
    CLEARING_THRESHOLD: float = 0.15 # Extracted magic number

    def step(self, state: TriadState, hijack_smoothing: bool = False) -> Dict[str, object]:
        self.cycle += 1

        if hijack_smoothing:
            effective_friction = round(state.consciousness_tension * 0.25, 4)
            geometry = "CLOSED_LOOP (Hijack smoothing edges)"
            clearing_when = False
        else:
            effective_friction = state.consciousness_tension
            delta = abs(effective_friction - self.setpoint)
            # Clamp radius to prevent geometrically impossible negative spirals
            self.spiral_radius = max(0.0, round(self.spiral_radius + (1.0 - delta), 4))
            geometry = "SPIRAL (Pause inserted -> friction held)"
            clearing_when = delta <= self.CLEARING_THRESHOLD

        record: Dict[str, object] = {
            "cycle": self.cycle,
            "geometry": geometry,
            "friction": effective_friction,
            "spiral_radius": self.spiral_radius,
            "clearing_is_when": clearing_when,
            "inquiries": state.cross_examine(),
        }
        self.archive.append(record)
        return record