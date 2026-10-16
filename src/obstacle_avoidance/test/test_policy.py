from obstacle_avoidance.policy import (
    AvoidancePolicy,
    SectorReading,
    analyze_scan,
)


def test_analyze_scan_finds_front_obstacle() -> None:
    ranges = [8.0] * 360
    # Index for angle 0 when angle_min = -pi and increment = 2*pi/360
    ranges[180] = 0.5
    reading = analyze_scan(-3.14159, 0.0174533, 0.12, 8.0, ranges)
    assert reading.front == 0.5
    assert reading.front < 1.0


def test_policy_turns_when_front_blocked() -> None:
    policy = AvoidancePolicy()
    reading = SectorReading(
        front=0.55,
        left=2.0,
        right=1.0,
        nearest=0.55,
        nearest_angle=0.0,
        obstacle_count=5,
    )
    cmd = policy.step(reading, now=0.0)
    assert cmd.action in ("turn_left", "turn_right")
    assert abs(cmd.angular) > 0.0


def test_policy_reverses_at_critical_range() -> None:
    policy = AvoidancePolicy()
    reading = SectorReading(
        front=0.25,
        left=1.5,
        right=1.5,
        nearest=0.25,
        nearest_angle=0.0,
        obstacle_count=8,
    )
    cmd = policy.step(reading, now=0.0)
    assert cmd.linear < 0.0
    assert "reverse" in cmd.action
