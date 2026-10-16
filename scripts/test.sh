#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose run --rm --entrypoint bash virtual-robot -lc '
  source /opt/ros/humble/setup.bash
  cd /home/ubuntu/workspace
  colcon build --symlink-install --packages-select obstacle_avoidance
  source install/setup.bash
  python3 -m pytest src/obstacle_avoidance/test -q
'
