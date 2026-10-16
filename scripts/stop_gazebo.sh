#!/usr/bin/env bash
# Stop all Gazebo processes before a fresh launch (fixes gzserver exit 255).
killall gzclient 2>/dev/null || true
killall gzserver 2>/dev/null || true
sleep 1
if pgrep gzserver >/dev/null 2>&1; then
  killall -9 gzserver 2>/dev/null || true
fi
if pgrep gzclient >/dev/null 2>&1; then
  killall -9 gzclient 2>/dev/null || true
fi
echo "Gazebo stopped. Wait 2 seconds, then launch again."
