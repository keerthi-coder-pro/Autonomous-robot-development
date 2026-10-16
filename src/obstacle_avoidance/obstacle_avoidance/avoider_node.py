"""Reactive obstacle avoidance controller."""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import String

from obstacle_avoidance.policy import AvoidanceConfig, AvoidancePolicy, SectorReading
from virtual_robot_msgs.msg import ObstacleReport


class ObstacleAvoider(Node):
    def __init__(self) -> None:
        super().__init__("obstacle_avoider")
        self._config = AvoidanceConfig(
            critical_range=self._param("critical_range", 0.35),
            stop_range=self._param("stop_range", 0.70),
            slow_range=self._param("slow_range", 1.15),
            recover_range=self._param("recover_range", 1.05),
            side_influence=self._param("side_influence", 0.85),
            forward_speed=self._param("forward_speed", 0.22),
            slow_speed=self._param("slow_speed", 0.10),
            reverse_speed=self._param("reverse_speed", 0.08),
            turn_speed=self._param("turn_speed", 0.90),
            side_bias=self._param("side_bias", 0.35),
            commit_seconds=self._param("commit_seconds", 0.55),
            critical_commit_seconds=self._param("critical_commit_seconds", 1.2),
            side_switch_margin=self._param("side_switch_margin", 0.25),
        )
        self.declare_parameter("report_timeout", 1.0)
        self._timeout = float(self.get_parameter("report_timeout").value)
        self._policy = AvoidancePolicy(self._config)
        self._last_report = None
        self._last_action: str | None = None
        self.declare_parameter("log_on_change", True)
        self.declare_parameter("log_every_tick", False)
        self._log_on_change = bool(self.get_parameter("log_on_change").value)
        self._log_every_tick = bool(self.get_parameter("log_every_tick").value)
        self._cmd = self.create_publisher(Twist, "cmd_vel", 10)
        self._action = self.create_publisher(String, "avoidance_action", 10)
        self.create_subscription(ObstacleReport, "obstacle_report", self._on_report, 10)
        self.create_timer(0.1, self._tick)

    def _param(self, name: str, default: float) -> float:
        self.declare_parameter(name, default)
        return float(self.get_parameter(name).value)

    def _on_report(self, msg: ObstacleReport) -> None:
        self._last_report = msg

    def _stop(self, action: str) -> None:
        command = Twist()
        self._cmd.publish(command)
        notice = String()
        notice.data = action
        self._action.publish(notice)

    def _tick(self) -> None:
        report = self._last_report
        if report is None:
            self._stop("wait")
            return
        age = (self.get_clock().now() - rclpy.time.Time.from_msg(report.header.stamp)).nanoseconds / 1e9
        if report.header.stamp.sec == 0 and report.header.stamp.nanosec == 0:
            age = 0.0
        if age > self._timeout:
            self._stop("stop_timeout")
            return

        reading = SectorReading(
            front=report.front_range,
            left=report.left_range,
            right=report.right_range,
            nearest=report.nearest_range,
            nearest_angle=report.nearest_angle,
            obstacle_count=report.obstacle_count,
        )
        now = self.get_clock().now().nanoseconds / 1e9
        decision = self._policy.step(reading, now)
        command = Twist()
        command.linear.x = float(decision.linear)
        command.angular.z = float(decision.angular)
        self._cmd.publish(command)
        notice = String()
        notice.data = decision.action
        if self._last_action != decision.action:
            self._action.publish(notice)
            if self._log_on_change:
                prev = self._last_action if self._last_action is not None else "(start)"
                self.get_logger().info(
                    f"DIRECTION CHANGE: {prev} -> {decision.action} | "
                    f"front={reading.front:.2f}m left={reading.left:.2f}m "
                    f"right={reading.right:.2f}m | "
                    f"linear={decision.linear:.2f} angular={decision.angular:.2f}"
                )
            self._last_action = decision.action
        elif self._log_every_tick:
            self.get_logger().info(
                f"{decision.action} linear={decision.linear:.2f} "
                f"angular={decision.angular:.2f}",
                throttle_duration_sec=2.0,
            )


def main() -> None:
    rclpy.init()
    node = ObstacleAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
