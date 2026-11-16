import sys
from coniunctio_engine import ConiunctioEngine


def print_banner():
    print("=" * 60)
    print("       CONIUNCTIO ENGINE v0.2 — INTERACTIVE SANDBOX       ")
    print("=" * 60)
    print("Enter thought, feeling, and instinct values (e.g., 0.2, 0.3, 0.1)")
    print("Type 'history' to view past cycles, 'reset' to clear, or 'exit' to quit.\n")


def interactive_sandbox():
    engine = ConiunctioEngine()
    print_banner()

    while True:
        try:
            user_input = input("coniunctio> ").strip()
            
            if not user_input:
                continue
            if user_input.lower() == "exit":
                print("Exiting sandbox. The spine holds the tension. *88*")
                break
            if user_input.lower() == "reset":
                engine = ConiunctioEngine()
                print("-> Engine re-initialized to base GroundState.\n")
                continue
            if user_input.lower() == "history":
                print(f"\n--- Trajectory History ({len(engine.history)} cycles) ---")
                for rec in engine.history:
                    print(
                        f"Cycle {rec['cycle']} | State: {rec['state']:<12} | "
                        f"Depth: {rec['spiral_depth']} | Coherence: {rec['coherence']:.4f} | "
                        f"Input: {rec['input']}"
                    )
                print("-" * 50 + "\n")
                continue

            # Parse comma-separated values
            parts = [float(x.strip()) for x in user_input.split(",")]
            if len(parts) != 3:
                print("Error: Please provide exactly 3 comma-separated numbers (e.g., 0.2, 0.25, 0.15).")
                continue

            t, f, i = parts
            rec = engine.step(t, f, i)

            print(
                f"   [Cycle {rec['cycle']}] State: {rec['state']} | "
                f"Depth: {rec['spiral_depth']} | Coherence: {rec['coherence']:.4f} | "
                f"Tension: {rec['tension']:.4f}"
            )
            print(f"   Adaptive Prior: {rec['prior']}\n")

        except ValueError:
            print("Error: Invalid numeric format. Use commas like: 0.2, 0.3, 0.1")
        except KeyboardInterrupt:
            print("\nExiting sandbox.")
            break


if __name__ == "__main__":
    interactive_sandbox()
