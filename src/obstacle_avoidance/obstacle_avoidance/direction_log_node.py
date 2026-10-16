"""Print a clear line in the terminal whenever avoidance mode / direction changes."""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import String

from virtual_robot_msgs.msg import ObstacleReport


class DirectionLogNode(Node):
    def __init__(self) -> None:
        super().__init__("direction_logger")
        self._last_action: str | None = None
        self._last_report: ObstacleReport | None = None
        self._last_cmd = Twist()
        self.create_subscription(ObstacleReport, "obstacle_report", self._on_report, 10)
        self.create_subscription(Twist, "cmd_vel", self._on_cmd, 10)
        self.create_subscription(String, "avoidance_action", self._on_action, 10)
        self.get_logger().info(
            "Direction logger started — waiting for /avoidance_action changes..."
        )

    def _on_report(self, msg: ObstacleReport) -> None:
        self._last_report = msg

    def _on_cmd(self, msg: Twist) -> None:
        self._last_cmd = msg

    def _on_action(self, msg: String) -> None:
        action = msg.data
        if action == self._last_action:
            return
        previous = self._last_action if self._last_action is not None else "(start)"
        self._last_action = action
        stamp = self.get_clock().now().nanoseconds / 1e9
        report = self._last_report
        if report is not None:
            self.get_logger().info(
                f"[{stamp:8.2f}s] DIRECTION CHANGE: {previous} -> {action} | "
                f"front={report.front_range:.2f}m left={report.left_range:.2f}m "
                f"right={report.right_range:.2f}m nearest={report.nearest_range:.2f}m | "
                f"cmd_vel linear={self._last_cmd.linear.x:.2f} "
                f"angular={self._last_cmd.angular.z:.2f}"
            )
        else:
            self.get_logger().info(
                f"[{stamp:8.2f}s] DIRECTION CHANGE: {previous} -> {action}"
            )


def main() -> None:
    rclpy.init()
    node = DirectionLogNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
