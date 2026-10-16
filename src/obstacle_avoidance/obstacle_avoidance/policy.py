"""Pure obstacle detection and avoidance policy.

No ROS imports, so the behaviour can be tested without Gazebo.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


NO_HIT = 8.0
FRONT_HALF_ANGLE = 0.50
SIDE_OUTER_ANGLE = 1.40
FORWARD_HALF = math.pi / 2
COUNT_RANGE = 1.5


@dataclass
class SectorReading:
    front: float
    left: float
    right: float
    nearest: float
    nearest_angle: float
    obstacle_count: int


@dataclass
class AvoidanceConfig:
    critical_range: float = 0.35
    stop_range: float = 0.70
    slow_range: float = 1.15
    recover_range: float = 1.05
    side_influence: float = 0.85
    forward_speed: float = 0.22
    slow_speed: float = 0.10
    reverse_speed: float = 0.08
    turn_speed: float = 0.90
    side_bias: float = 0.35
    commit_seconds: float = 0.55
    critical_commit_seconds: float = 1.2
    side_switch_margin: float = 0.25


@dataclass
class DriveCommand:
    linear: float
    angular: float
    action: str


def _wrap(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


def _valid_range(distance: float, range_min: float, range_max: float) -> bool:
    return (
        math.isfinite(distance)
        and distance > range_min
        and distance < range_max
    )


def analyze_scan(
    angle_min: float,
    angle_increment: float,
    range_min: float,
    range_max: float,
    ranges: list[float],
) -> SectorReading:
    """Reduce a lidar sweep to front, left, and right clearances."""
    front: list[float] = []
    left: list[float] = []
    right: list[float] = []
    nearest = NO_HIT
    nearest_angle = 0.0
    obstacle_count = 0

    for index, distance in enumerate(ranges):
        angle = _wrap(angle_min + index * angle_increment)
        if not _valid_range(distance, range_min, range_max):
            continue
        if -FRONT_HALF_ANGLE <= angle <= FRONT_HALF_ANGLE:
            front.append(distance)
        elif FRONT_HALF_ANGLE < angle <= SIDE_OUTER_ANGLE:
            left.append(distance)
        elif -SIDE_OUTER_ANGLE <= angle < -FRONT_HALF_ANGLE:
            right.append(distance)
        if -FORWARD_HALF <= angle <= FORWARD_HALF:
            if distance < nearest:
                nearest = distance
                nearest_angle = angle
            if distance < COUNT_RANGE:
                obstacle_count += 1

    return SectorReading(
        front=min(front) if front else NO_HIT,
        left=min(left) if left else NO_HIT,
        right=min(right) if right else NO_HIT,
        nearest=nearest,
        nearest_angle=nearest_angle,
        obstacle_count=obstacle_count,
    )


class AvoidancePolicy:
    """Drive forward, and turn toward the clearer side when the front is blocked.

    A short commit window keeps the robot from oscillating when both sides
    look similar.
    """

    def __init__(self, config: AvoidanceConfig | None = None) -> None:
        self.config = config or AvoidanceConfig()
        self._turn = 1.0
        self._commit_until = 0.0

    def _clearer_side(self, reading: SectorReading) -> float:
        margin = self.config.side_switch_margin
        diff = reading.left - reading.right
        if abs(diff) < margin:
            return self._turn if self._turn != 0.0 else 1.0
        return 1.0 if diff > 0 else -1.0

    def step(self, reading: SectorReading, now: float) -> DriveCommand:
        config = self.config
        turning = now < self._commit_until and reading.front < config.recover_range

        if reading.front < config.critical_range:
            if now >= self._commit_until:
                self._turn = self._clearer_side(reading)
                self._commit_until = now + config.critical_commit_seconds
            action = "reverse_left" if self._turn > 0 else "reverse_right"
            return DriveCommand(
                linear=-config.reverse_speed,
                angular=config.turn_speed * self._turn,
                action=action,
            )

        if reading.front < config.stop_range or turning:
            if not turning:
                self._turn = self._clearer_side(reading)
                self._commit_until = now + config.commit_seconds
            action = "turn_left" if self._turn > 0 else "turn_right"
            return DriveCommand(
                linear=0.02,
                angular=config.turn_speed * self._turn,
                action=action,
            )

        bias = 0.0
        if reading.left < config.side_influence and reading.left < reading.right:
            bias = -config.side_bias
        elif reading.right < config.side_influence and reading.right < reading.left:
            bias = config.side_bias

        if reading.front < config.slow_range:
            return DriveCommand(config.slow_speed, bias, "slow")
        return DriveCommand(config.forward_speed, bias, "forward")
