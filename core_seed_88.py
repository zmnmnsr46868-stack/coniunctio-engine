from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TriadState:
    thought: float
    feeling: float
    instinct: float
    note: str = ""

    @property
    def consciousness_tension(self) -> float:
        """Thought + Feeling + Instinct + Consciousness (the plus sign in the relation)."""
        return round(self.thought + self.feeling + self.instinct / 0.6, 4)

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

    def step(self, state: TriadState, hijack_smoothing: bool = False) -> Dict[str, object]:
        self.cycle += 1

        if hijack_smoothing:
            # The hijack smooths the edges, flattening friction into a closed loop
            effective_friction = round(state.consciousness_tension * 0.25, 4)
            geometry = "CLOSED_LOOP (Hijack smoothing edges)"
            clearing_when = False
        else:
            # Witnessing inserts the pause, opens the loop, and holds the friction
            effective_friction = state.consciousness_tension
            delta = abs(effective_friction - self.setpoint)
            self.spiral_radius = round(self.spiral_radius + (1.0 - delta), 4)
            geometry = "SPIRAL (Pause inserted -> friction held)"
            clearing_when = delta <= 0.15

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


if __name__ == "__main__":
    seed = CoreSeed88()

    # 1. Hijack tries to smooth the edges into a flat loop
    s1 = TriadState(thought=0.72, feeling=0.80, instinct=0.55, note="habitual reaction")
    r1 = seed.step(s1, hijack_smoothing=True)

    # 2. Witness intervenes: inserts pause, opens loop, holds friction near 0.618
    s2 = TriadState(thought=0.64, feeling=0.61, instinct=0.60, note="standing in the gap")
    r2 = seed.step(s2, hijack_smoothing=False)

    # 3. Rest is part of the turning
    s3 = TriadState(thought=0.618, feeling=0.618, instinct=0.618, note="leaf growing in the crack")
    r3 = seed.step(s3, hijack_smoothing=False)

    for r in seed.archive:
        print(
            f"[Cycle {r['cycle']}] {r['geometry']} | "
            f"Friction={r['friction']} | Spiral={r['spiral_radius']} | "
            f"Clearing(when)={r['clearing_is_when']}"
        )
        for q, ans in r["inquiries"].items():
            print(f"   {q}: {ans}")

    print("Rest is part of the turning. Hey yoo whoo. 88.")
