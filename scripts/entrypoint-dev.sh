#!/bin/bash
set -eo pipefail

WORKSPACE=/home/ubuntu/workspace

if [ -d "${WORKSPACE}/src" ]; then
  cd "${WORKSPACE}"
  if [ ! -f install/setup.bash ] || find src -newer install/setup.bash -print -quit | grep -q .; then
    echo "[virtual-robot] Building ROS 2 workspace..."
    set +u
    source /opt/ros/humble/setup.bash
    set +e
    colcon build --symlink-install
  fi
fi

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

exec /bin/bash -c "/entrypoint.sh"
