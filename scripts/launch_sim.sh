#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash scripts/stop_gazebo.sh
sleep 2
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch virtual_robot_bringup bringup.launch.py
