import glob
import json
import os
import sys

PHI_INV = 0.618


def load_trajectory(filepath=None):
    """Loads a specific trajectory JSON file or automatically picks the most recent export."""
    if not filepath:
        files = sorted(glob.glob("trajectory_*.json"), key=os.path.getmtime)
        if not files:
            print("No trajectory_*.json files found. Run 'export' in sandbox.py first.")
            sys.exit(1)
        filepath = files[-1]

    with open(filepath, "r", encoding="utf-8") as f:
        return filepath, json.load(f)


def render_ascii_chart(history):
    """Draws a terminal-native coherence timeline against the 0.618 threshold."""
    print("\n--- Coherence Timeline (Threshold = 0.618) ---")
    bar_width = 40
    threshold_pos = int(PHI_INV * bar_width)

    for rec in history:
        c = rec["coherence"]
        filled = int(c * bar_width)
        bar = [" "] * (bar_width + 1)

        for i in range(filled):
            bar[i] = "█" if rec["state"] == "SPIRAL" else "▒"

        # Mark the golden ratio conjugate threshold
        bar[threshold_pos] = "|"
        bar_str = "".join(bar)
        print(f"C{rec['cycle']:02d} [{bar_str}] {c:.4f} ({rec['state']})")


def analyze(filepath=None):
    path, history = load_trajectory(filepath)
    if not history:
        print(f"File '{path}' contains no cycle records.")
        return

    total = len(history)
    spirals = sum(1 for r in history if r["state"] == "SPIRAL")
    resets = total - spirals
    max_depth = max(r["spiral_depth"] for r in history)
    avg_coherence = sum(r["coherence"] for r in history) / total
    peak_tension = max(r["tension"] for r in history)

    # Calculate average absolute intensity across Thought, Feeling, Instinct
    axes = ["Thought", "Feeling", "Instinct"]
    means = [
        sum(abs(r["input"][idx]) for r in history) / total
        for idx in range(3)
    ]
    dominant_axis = axes[means.index(max(means))]

    print("=" * 64)
    print(f"  CONIUNCTIO TRAJECTORY ANALYSIS: {os.path.basename(path)}")
    print("=" * 64)
    print(f"  Total Cycles       : {total}")
    print(f"  Spiral Phase-Locks : {spirals} ({(spirals / total) * 100:.1f}%)")
    print(f"  Ground Resets      : {resets} ({(resets / total) * 100:.1f}%)")
    print(f"  Max Spiral Depth   : {max_depth}")
    print(f"  Mean Coherence     : {avg_coherence:.4f}")
    print(f"  Peak Tension Spike : {peak_tension:.4f}")
    print(f"  Dominant Polarity  : {dominant_axis} (avg magnitude {max(means):.3f})")

    render_ascii_chart(history)
    print("=" * 64 + "\n")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    analyze(target)
