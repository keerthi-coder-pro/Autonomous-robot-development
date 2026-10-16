#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose run --rm --entrypoint bash virtual-robot -lc '
  source /opt/ros/humble/setup.bash
  cd /home/ubuntu/workspace
  colcon build --symlink-install
'
