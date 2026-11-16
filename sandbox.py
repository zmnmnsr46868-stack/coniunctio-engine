import json
import time
from typing import Any
from coniunctio_engine import ConiunctioEngine


def run_preset_ramp(engine: ConiunctioEngine) -> None:
    """Preset 1: Gradual Individuation Ramp. Slowly scales vectors to test phase-lock endurance."""
    print("\n[Preset] Running Gradual Individuation Ramp...")
    steps = [
        (0.1, 0.1, 0.1), (0.15, 0.2, 0.15), (0.2, 0.25, 0.2),
        (0.3, 0.3, 0.25), (0.4, 0.35, 0.3), (0.5, 0.4, 0.35)
    ]
    for t, f, i in steps:
        rec = engine.step(t, f, i)
        print(f"Cycle {rec['cycle']} | State: {rec['state']} | Coherence: {rec['coherence']} | Depth: {rec['spiral_depth']}")
    print("Ramp preset complete.")


def run_preset_rupture(engine: ConiunctioEngine) -> None:
    """Preset 2: Sudden Rupture & Re-Integration. Builds depth, injects shock, and tracks recovery."""
    print("\n[Preset] Running Sudden Rupture & Re-Integration...")
    for _ in range(5):
        rec = engine.step(0.2, 0.2, 0.2)
        print(f"Cycle {rec['cycle']} | State: {rec['state']} | Depth: {rec['spiral_depth']}")
    
    print(">>> Injecting high-tension shock vector [4.0, -4.0, 4.0]...")
    rec = engine.step(4.0, -4.0, 4.0)
    print(f"Cycle {rec['cycle']} | State: {rec['state']} | Coherence: {rec['coherence']} | Depth: {rec['spiral_depth']}")
    
    print(">>> Re-integrating baseline inputs...")
    for _ in range(3):
        rec = engine.step(0.2, 0.2, 0.2)
        print(f"Cycle {rec['cycle']} | State: {rec['state']} | Coherence: {rec['coherence']} | Depth: {rec['spiral_depth']}")
    print("Rupture preset complete.")


def run_preset_oscillate(engine: ConiunctioEngine) -> None:
    """Preset 3: Oscillating Polarity Drift. Alternates between dominant thought and feeling."""
    print("\n[Preset] Running Oscillating Polarity Drift...")
    sequence = [
        (0.4, 0.0, 0.0),
        (0.0, 0.4, 0.0),
        (0.4, 0.0, 0.0),
        (0.0, 0.4, 0.0),
        (0.2, 0.2, 0.1)
    ]
    for t, f, i in sequence:
        rec = engine.step(t, f, i)
        print(f"Cycle {rec['cycle']} | State: {rec['state']} | Prior: {rec['prior']} | Coherence: {rec['coherence']}")
    print("Oscillation preset complete.")


def interactive_repl() -> None:
    engine = ConiunctioEngine()
    print("=== Coniunctio Engine v0.2.1 Sandbox REPL ===")
    print("Commands:")
    print("  t, f, i         -> Step engine with comma-separated values (e.g., 0.2, 0.3, 0.1)")
    print("  demo ramp       -> Run Gradual Individuation Ramp preset")
    print("  demo rupture    -> Run Sudden Rupture & Re-Integration preset")
    print("  demo oscillate  -> Run Oscillating Polarity Drift preset")
    print("  status          -> Display current engine session statistics")
    print("  export          -> Save session history to JSON")
    print("  reset           -> Reset engine state")
    print("  exit            -> Quit sandbox\n")

    while True:
        try:
            cmd = input("coniunctio> ").strip()
            if not cmd:
                continue
            if cmd.lower() == "exit":
                print("Exiting sandbox.")
                break
            elif cmd.lower() == "reset":
                engine = ConiunctioEngine()
                print("Engine re-initialized to GroundState.")
                continue
            elif cmd.lower() == "status":
                print(f"Cycles: {len(engine.history)} | Spiral Depth: {engine.spiral_depth} | Prior: {[round(x, 4) for x in engine.prior]}")
                continue
            elif cmd.lower() == "export":
                if not engine.history:
                    print("Nothing to export yet. Run a preset or enter a vector first.")
                    continue
                filename = f"trajectory_{int(time.time())}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(engine.history, f, indent=2)
                print(f"History successfully exported to {filename}")
                continue
            elif cmd.lower() == "demo ramp":
                run_preset_ramp(engine)
                continue
            elif cmd.lower() == "demo rupture":
                run_preset_rupture(engine)
                continue
            elif cmd.lower() == "demo oscillate":
                run_preset_oscillate(engine)
                continue

            parts = [float(x.strip()) for x in cmd.split(",")]
            if len(parts) != 3:
                print("Error: Please provide exactly 3 comma-separated numbers (thought, feeling, instinct).")
                continue

            rec = engine.step(parts[0], parts[1], parts[2])
            print(f"[{rec['state']}] Cycle {rec['cycle']} | Tension: {rec['tension']} | Coherence: {rec['coherence']} | Spiral Depth: {rec['spiral_depth']} | Prior: {rec['prior']}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting sandbox.")
            break
        except ValueError as e:
            print(f"Input Error: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    interactive_repl()
