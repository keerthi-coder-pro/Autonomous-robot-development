#!/usr/bin/env python3
"""Generate a 2x3 presentation dashboard (similar layout to viva examples).

Run on Mac or inside Ubuntu:
  python3 scripts/generate_presentation_graphs.py

Output: docs/graphs/presentation_dashboard.png (+ individual plots)
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "docs" / "graphs"
STOP_THRESHOLD = 0.70
CRITICAL = 0.35
DURATION = 400.0
DT = 1.0


def simulate_run() -> dict[str, np.ndarray]:
    """Coherent synthetic run for demo slides (matches project logic)."""
    n = int(DURATION / DT) + 1
    t = np.arange(n) * DT
    x = np.zeros(n)
    y = np.zeros(n)
    speed = np.zeros(n)
    nearest = np.full(n, 3.0)
    front = np.full(n, 3.0)
    state_idx = np.zeros(n, dtype=int)  # 0 explore 1 slow 2 turn 3 reverse 4 stop
    states = ["forward", "slow", "turn", "reverse", "stop"]

    heading = 0.0
    px, py = -3.2, -3.2
    for i in range(n):
        ti = t[i]
        # Piecewise scenario: explore, hit obstacle, turn, continue
        if ti < 80:
            front[i], nearest[i] = 2.2 + 0.3 * math.sin(ti / 12), 2.0 + 0.2 * math.cos(ti / 15)
            speed[i], state_idx[i] = 0.22, 0
            heading += 0.002
        elif ti < 120:
            front[i] = max(0.28, 2.0 - (ti - 80) * 0.04)
            nearest[i] = front[i]
            speed[i] = 0.10 if front[i] > CRITICAL else -0.08
            state_idx[i] = 1 if front[i] > CRITICAL else 3
            heading += 0.04 if front[i] > CRITICAL else -0.02
        elif ti < 180:
            front[i], nearest[i] = 1.2 + 0.4 * math.sin(ti / 10), 1.0 + 0.3 * math.sin(ti / 8)
            speed[i], state_idx[i] = 0.10, 2
            heading += 0.06
        elif ti < 280:
            front[i] = 1.8 + 0.5 * math.sin(ti / 25)
            nearest[i] = min(front[i], 1.4 + 0.2 * math.sin(ti / 18))
            speed[i], state_idx[i] = 0.22, 0
            heading += 0.015
        elif ti < 320:
            front[i] = max(0.32, 0.85 - (ti - 280) * 0.012)
            nearest[i] = front[i]
            speed[i] = -0.08 if front[i] < CRITICAL else 0.02
            state_idx[i] = 3 if front[i] < CRITICAL else 2
            heading += 0.05
        else:
            front[i], nearest[i] = 2.5, 2.2
            speed[i], state_idx[i] = 0.22, 0
            heading += 0.008

        px += speed[i] * math.cos(heading) * DT
        py += speed[i] * math.sin(heading) * DT
        x[i], y[i] = px, py

    return {
        "t": t,
        "x": x,
        "y": y,
        "speed": speed,
        "nearest": nearest,
        "front": front,
        "state_idx": state_idx,
        "states": states,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    d = simulate_run()
    t, x, y = d["t"], d["x"], d["y"]
    speed, nearest, front = d["speed"], d["nearest"], d["front"]
    state_idx, states = d["state_idx"], d["states"]

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle(
        "Virtual Autonomous Robot — ROS2 & Gazebo\n"
        "Obstacle detection & avoidance (demo run)",
        fontsize=13,
        fontweight="bold",
    )

    # 1 — Path coloured by time
    ax = axes[0, 0]
    sc = ax.scatter(x, y, c=t, cmap="viridis", s=8, linewidths=0)
    ax.plot(x, y, color="gray", alpha=0.25, linewidth=0.8)
    ax.set_title("Robot path (colour = time)")
    ax.set_xlabel("X position (m)")
    ax.set_ylabel("Y position (m)")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    plt.colorbar(sc, ax=ax, label="Time (s)")

    # 2 — Forward speed
    ax = axes[0, 1]
    ax.plot(t, speed, color="#2563eb", linewidth=1.2)
    ax.set_title("Robot forward speed")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Linear velocity (m/s)")
    ax.grid(True, alpha=0.3)

    # 3 — Nearest obstacle + threshold
    ax = axes[0, 2]
    ax.plot(t, nearest, color="#0ea5e9", linewidth=1.2, label="Nearest (Lidar)")
    ax.axhline(STOP_THRESHOLD, color="red", linestyle="--", linewidth=1.2, label="Stop threshold")
    ax.axhline(CRITICAL, color="darkred", linestyle=":", linewidth=1.0, label="Critical")
    ax.set_title("Nearest obstacle distance (Lidar)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Distance (m)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # 4 — Front sector (main detection signal)
    ax = axes[1, 0]
    ax.plot(t, front, color="#f97316", linewidth=1.2, label="Front range")
    ax.plot(t, nearest, color="#64748b", linewidth=0.9, alpha=0.7, label="Nearest")
    ax.axhline(STOP_THRESHOLD, color="red", linestyle="--", linewidth=1.0)
    ax.set_title("Front clearance (obstacle detection)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Distance (m)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 5 — Decision state
    ax = axes[1, 1]
    ax.step(t, state_idx, where="post", color="#dc2626", linewidth=1.5)
    ax.set_yticks(range(len(states)))
    ax.set_yticklabels(states)
    ax.set_title("Decision state over time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Avoidance mode")
    ax.grid(True, alpha=0.3)

    # 6 — Blocked flag timeline
    blocked = (front < STOP_THRESHOLD).astype(float)
    ax = axes[1, 2]
    ax.fill_between(t, 0, blocked, step="post", color="#ef4444", alpha=0.5, label="Front blocked")
    ax.plot(t, (nearest < STOP_THRESHOLD).astype(float), color="#b91c1c", drawstyle="steps-post", label="Nearest < threshold")
    ax.set_title("Obstacle alert timeline")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Alert (0/1)")
    ax.set_ylim(-0.05, 1.15)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.3)

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    dashboard = OUT / "presentation_dashboard.png"
    fig.savefig(dashboard, dpi=160)
    plt.close(fig)

    # Keep earlier single plots updated from same data
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, front, label="Front range (m)", linewidth=2)
    ax.plot(t, nearest, label="Nearest obstacle (m)", linestyle="--")
    ax.axhline(STOP_THRESHOLD, color="red", linestyle="--", label="Stop threshold")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Distance (m)")
    ax.set_title("Obstacle detection — lidar sector ranges")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "obstacle_ranges.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, speed, color="#2563eb", linewidth=2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Linear velocity (m/s)")
    ax.set_title("Robot motion commands (/cmd_vel linear.x)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "velocity_commands.png", dpi=150)
    plt.close(fig)

    print(f"Saved: {dashboard}")
    print(f"Saved: {OUT / 'obstacle_ranges.png'}")
    print(f"Saved: {OUT / 'velocity_commands.png'}")


if __name__ == "__main__":
    main()
