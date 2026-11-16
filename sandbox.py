import json
import time
from coniunctio_engine import ConiunctioEngine

PRESETS = {
    "spiral": [
        (0.20, 0.25, 0.15),
        (0.25, 0.30, 0.20),
        (0.30, 0.35, 0.25),
        (0.35, 0.40, 0.30),
    ],
    "shock": [
        (0.20, 0.20, 0.20),
        (0.22, 0.22, 0.22),
        (0.95, 0.90, 0.85),  # High tension triggers GROUND_RESET
        (0.15, 0.15, 0.15),
    ],
}


def print_banner():
    print("=" * 64)
    print("       CONIUNCTIO ENGINE v0.2 — INTERACTIVE SANDBOX       ")
    print("=" * 64)
    print("Enter thought, feeling, and instinct values (e.g., 0.2, 0.3, 0.1)")
    print("Commands:")
    print("  demo    : Run a preset trajectory ('spiral' or 'shock')")
    print("  history : View past cycles")
    print("  export  : Save trajectory history to a JSON file")
    print("  reset   : Clear history and return to GroundState")
    print("  exit    : Quit the sandbox\n")


def print_step(rec):
    print(
        f"   [Cycle {rec['cycle']}] State: {rec['state']} | "
        f"Depth: {rec['spiral_depth']} | Coherence: {rec['coherence']:.4f} | "
        f"Tension: {rec['tension']:.4f}"
    )
    print(f"   Adaptive Prior: {rec['prior']}\n")


def interactive_sandbox():
    engine = ConiunctioEngine()
    print_banner()

    while True:
        try:
            user_input = input("coniunctio> ").strip()
            cmd = user_input.lower()

            if not user_input:
                continue

            if cmd == "exit":
                print("Exiting sandbox. The spine holds the tension. *88*")
                break

            if cmd == "reset":
                engine = ConiunctioEngine()
                print("-> Engine re-initialized to base GroundState.\n")
                continue

            if cmd == "history":
                if not engine.history:
                    print("-> No cycles recorded yet.\n")
                    continue
                print(f"\n--- Trajectory History ({len(engine.history)} cycles) ---")
                for rec in engine.history:
                    print(
                        f"Cycle {rec['cycle']} | State: {rec['state']:<12} | "
                        f"Depth: {rec['spiral_depth']} | Coherence: {rec['coherence']:.4f} | "
                        f"Input: {rec['input']}"
                    )
                print("-" * 55 + "\n")
                continue

            if cmd == "export":
                if not engine.history:
                    print("-> Nothing to export yet. Run some cycles first.\n")
                    continue
                filename = f"trajectory_{int(time.time())}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(engine.history, f, indent=2)
                print(f"-> Exported {len(engine.history)} cycles to {filename}\n")
                continue

            if cmd.startswith("demo"):
                parts = cmd.split()
                preset_name = parts[1] if len(parts) > 1 else "spiral"
                if preset_name not in PRESETS:
                    print(f"Error: Unknown preset '{preset_name}'. Choose 'spiral' or 'shock'.\n")
                    continue
                print(f"-> Running '{preset_name}' preset trajectory...")
                for t, f, i in PRESETS[preset_name]:
                    print(f"   Input: ({t}, {f}, {i})")
                    rec = engine.step(t, f, i)
                    print_step(rec)
                continue

            # Parse comma-separated values
            parts = [float(x.strip()) for x in user_input.split(",")]
            if len(parts) != 3:
                print("Error: Please provide 3 comma-separated numbers (e.g., 0.2, 0.25, 0.15).\n")
                continue

            t, f, i = parts
            rec = engine.step(t, f, i)
            print_step(rec)

        except ValueError:
            print("Error: Invalid numeric format. Use commas like: 0.2, 0.3, 0.1\n")
        except KeyboardInterrupt:
            print("\nExiting sandbox.")
            break


if __name__ == "__main__":
    interactive_sandbox()
