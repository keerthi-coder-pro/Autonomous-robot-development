# Logging direction changes and ROS / Gazebo output

## Fix: `gzserver` died (exit 255)

Usually **Gazebo is already running** or a previous crash left a process behind.

```bash
# Must stop BOTH — killing only gzclient leaves gzserver running → exit 255
bash ~/workspace/scripts/stop_gazebo.sh
sleep 2
ros2 launch virtual_robot_bringup bringup.launch.py
```

Or one command: `bash ~/workspace/scripts/launch_sim.sh`

Only run **one** launch at a time. If `spawn_entity` waits forever, gzserver did not start — fix that first.

---

## 1. Terminator — logs on direction change (built-in)

After rebuild, the avoider prints **`DIRECTION CHANGE: ... -> ...`** only when mode changes (forward, slow, turn_left, reverse, etc.):

```bash
source ~/workspace/install/setup.bash
colcon build --packages-select obstacle_avoidance --symlink-install
source install/setup.bash
ros2 launch virtual_robot_bringup bringup.launch.py
```

You will see lines like:

```text
[obstacle_avoider]: DIRECTION CHANGE: forward -> turn_left | front=0.55m ...
```

Toggle in `config/avoidance.yaml`: `log_on_change: true`, `log_every_tick: false`.

---

## 2. Second Terminator pane — dedicated direction logger

Split terminal (right-click → Split). Pane 2:

```bash
source ~/workspace/install/setup.bash
ros2 run obstacle_avoidance direction_logger
```

Only **changes** on `/avoidance_action` are printed with timestamp and lidar ranges.

---

## 3. Other ways to see the same data

| Method | Command / tool | What you see |
|--------|----------------|--------------|
| Echo action topic | `ros2 topic echo /avoidance_action` | Every published mode change |
| Echo velocity | `ros2 topic echo /cmd_vel` | linear.x, angular.z |
| Echo detection | `ros2 topic echo /obstacle_report` | front/left/right ranges |
| Record bag | `ros2 bag record /avoidance_action /cmd_vel /obstacle_report /scan` | Replay later with `ros2 bag play` |
| ROS log level | `ros2 run ... --ros-args --log-level debug` | More node debug output |
| Launch log files | `~/.ros/log/<latest-run>/` | All node stdout/stderr from launch |
| rqt | `rqt` → Plugins → Logging → Console | GUI log viewer (if installed) |

---

## 4. Gazebo-specific logging

| What | Where |
|------|--------|
| Gazebo server/client errors | Same Terminator as launch (gzserver/gzclient lines) |
| Verbose Gazebo | Add to launch or run `gzserver --verbose` |
| Model/sensor debug | Gazebo GUI → View → Transparent / Wireframe; lidar rays already visualised |
| Physics stats | Bottom bar in Gazebo (RTF, sim time, FPS) |
| Plugin output | Often appears as ROS logs from `diff_drive`, `gazebo_ros_lidar` |

Gazebo does **not** replace ROS logs for your algorithm — use ROS topics + `rclpy` loggers for detection/avoidance decisions.

---

## 5. Save logs to a file (for report / viva)

```bash
ros2 launch virtual_robot_bringup bringup.launch.py 2>&1 | tee ~/workspace/run_log.txt
```

Or only direction lines in pane 2:

```bash
ros2 run obstacle_avoidance direction_logger 2>&1 | tee ~/workspace/direction_log.txt
```
