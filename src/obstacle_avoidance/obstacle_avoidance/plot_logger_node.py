"""Record obstacle and velocity data, then save presentation graphs as PNG files."""

from __future__ import annotations

import os
from pathlib import Path

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from virtual_robot_msgs.msg import ObstacleReport


class PlotLogger(Node):
    def __init__(self) -> None:
        super().__init__("plot_logger")
        self.declare_parameter("duration_sec", 45.0)
        self.declare_parameter("output_dir", "/home/ubuntu/workspace/docs/graphs")
        self._duration = float(self.get_parameter("duration_sec").value)
        self._output_dir = Path(self.get_parameter("output_dir").value)
        self._t0 = self.get_clock().now().nanoseconds / 1e9
        self._times: list[float] = []
        self._front: list[float] = []
        self._left: list[float] = []
        self._right: list[float] = []
        self._nearest: list[float] = []
        self._linear: list[float] = []
        self._angular: list[float] = []
        self._last_cmd = Twist()
        self._last_report: ObstacleReport | None = None
        self._done = False
        self.create_subscription(
            ObstacleReport, "obstacle_report", self._on_report, 10
        )
        self.create_subscription(Twist, "cmd_vel", self._on_cmd, 10)
        self.create_timer(0.1, self._sample)
        self.create_timer(1.0, self._check_done)
        self.get_logger().info(
            f"Recording for {self._duration:.0f}s → {self._output_dir}"
        )

    def _elapsed(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9 - self._t0

    def _on_report(self, msg: ObstacleReport) -> None:
        self._last_report = msg

    def _check_done(self) -> None:
        if self._done or self._elapsed() < self._duration:
            return
        self._done = True
        self._save_plots()
        rclpy.shutdown()

    def _on_cmd(self, msg: Twist) -> None:
        self._last_cmd = msg

    def _sample(self) -> None:
        if self._last_report is None:
            return
        msg = self._last_report
        t = self._elapsed()
        self._times.append(t)
        self._front.append(msg.front_range)
        self._left.append(msg.left_range)
        self._right.append(msg.right_range)
        self._nearest.append(msg.nearest_range)
        self._linear.append(self._last_cmd.linear.x)
        self._angular.append(self._last_cmd.angular.z)

    def _save_plots(self) -> None:
        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            self.get_logger().error(
                "Install matplotlib: sudo apt install -y python3-matplotlib"
            )
            return

        if len(self._times) < 5:
            self.get_logger().warn("Not enough samples to plot.")
            return

        self._output_dir.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self._times, self._front, label="Front range (m)", linewidth=2)
        ax.plot(self._times, self._left, label="Left range (m)", linewidth=2)
        ax.plot(self._times, self._right, label="Right range (m)", linewidth=2)
        ax.plot(self._times, self._nearest, label="Nearest obstacle (m)", linestyle="--")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Distance (m)")
        ax.set_title("Obstacle detection — lidar sector ranges")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        path1 = self._output_dir / "obstacle_ranges.png"
        fig.savefig(path1, dpi=150)
        plt.close(fig)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        ax1.plot(self._times, self._linear, color="#2563eb", linewidth=2)
        ax1.set_ylabel("Linear velocity (m/s)")
        ax1.set_title("Robot motion commands (/cmd_vel)")
        ax1.grid(True, alpha=0.3)
        ax2.plot(self._times, self._angular, color="#dc2626", linewidth=2)
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Angular velocity (rad/s)")
        ax2.grid(True, alpha=0.3)
        fig.tight_layout()
        path2 = self._output_dir / "velocity_commands.png"
        fig.savefig(path2, dpi=150)
        plt.close(fig)

        self.get_logger().info(f"Saved {path1}")
        self.get_logger().info(f"Saved {path2}")


def main() -> None:
    rclpy.init()
    node = PlotLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node._save_plots()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
