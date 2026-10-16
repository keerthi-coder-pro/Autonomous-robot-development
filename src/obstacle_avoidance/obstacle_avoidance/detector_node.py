"""Lidar obstacle detector."""

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan

from obstacle_avoidance.policy import analyze_scan
from virtual_robot_msgs.msg import ObstacleReport


class ObstacleDetector(Node):
    def __init__(self) -> None:
        super().__init__("obstacle_detector")
        self.declare_parameter("stop_range", 0.70)
        self._stop_range = float(self.get_parameter("stop_range").value)
        self._pub = self.create_publisher(ObstacleReport, "obstacle_report", 10)
        self.create_subscription(LaserScan, "scan", self._on_scan, qos_profile_sensor_data)

    def _on_scan(self, msg: LaserScan) -> None:
        reading = analyze_scan(
            msg.angle_min,
            msg.angle_increment,
            msg.range_min,
            msg.range_max,
            list(msg.ranges),
        )
        report = ObstacleReport()
        report.header = msg.header
        report.front_range = float(reading.front)
        report.left_range = float(reading.left)
        report.right_range = float(reading.right)
        report.nearest_range = float(reading.nearest)
        report.nearest_angle = float(reading.nearest_angle)
        report.obstacle_count = int(reading.obstacle_count)
        report.front_blocked = reading.front < self._stop_range
        self._pub.publish(report)
        self.get_logger().info(
            f"front={reading.front:.2f}m left={reading.left:.2f}m "
            f"right={reading.right:.2f}m blocked={report.front_blocked}",
            throttle_duration_sec=2.0,
        )


def main() -> None:
    rclpy.init()
    node = ObstacleDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
