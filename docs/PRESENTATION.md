# Presentation guide (invigilator demo)

**Project title:** Development of a Virtual Autonomous Robot using ROS2 and Gazebo

## What to show (recommended order)

1. **Environment** — Ubuntu desktop (Docker/noVNC or native Linux).
2. **Simulation** — Gazebo arena, robot, lidar rays hitting obstacles.
3. **ROS 2 graph** — nodes and topics (architecture).
4. **Live or saved graphs** — obstacle distances and velocity over time.
5. **Short explanation** — detection (lidar sectors) → avoidance (cmd_vel).

## 1. Start simulation

```bash
source ~/workspace/install/setup.bash
ros2 launch virtual_robot_bringup bringup.launch.py
```

## 2. Show ROS 2 graph (for invigilator)

New terminal:

```bash
source ~/workspace/install/setup.bash
ros2 node list
ros2 topic list
rqt_graph
```

Explain: `obstacle_detector` reads `/scan`, `obstacle_avoider` sends `/cmd_vel`, Gazebo plugins bridge physics.

## 3. Graphs — two options

### Option A: Live plots (during demo)

```bash
sudo apt install -y ros-humble-rqt-plot   # once, if needed
rqt_plot /obstacle_report/front_range /obstacle_report/left_range /obstacle_report/right_range
```

Second window:

```bash
rqt_plot /cmd_vel/linear/x /cmd_vel/angular/z
```

### Option B: Save PNG files for slides (recommended)

While simulation is running, in another terminal:

```bash
source ~/workspace/install/setup.bash
sudo apt install -y python3-matplotlib   # once, if needed
ros2 run obstacle_avoidance plot_logger
```

After ~45 seconds, open:

- `docs/graphs/obstacle_ranges.png` — detection graph  
- `docs/graphs/velocity_commands.png` — avoidance / motion graph  

### Option C: Full 6-panel dashboard (like classmate’s slide)

On your Mac (or Ubuntu):

```bash
python3 scripts/generate_presentation_graphs.py
```

Open **`docs/graphs/presentation_dashboard.png`** — 6 graphs in one image:

| Panel | Meaning |
|-------|---------|
| Robot path (colour = time) | Motion from odometry-style trajectory |
| Robot forward speed | `/cmd_vel` linear.x |
| Nearest obstacle + red threshold | Lidar nearest distance vs stop line (0.7 m) |
| Front clearance | Main detection signal |
| Decision state | forward / slow / turn / reverse |
| Obstacle alert timeline | When front is “blocked” |

Show this in your PPT or PDF.

## 4. Talking points (30–60 seconds each)

| Topic | Say this |
|-------|----------|
| **Linux** | Ubuntu 22.04 hosts ROS 2 and Gazebo. |
| **ROS 2** | Nodes communicate via topics; modular detector and avoider. |
| **Gazebo** | Virtual robot with diff-drive and lidar in a cluttered world. |
| **Detection** | Lidar scan split into front / left / right clearances. |
| **Avoidance** | If front blocked, turn toward clearer side; reverse if too close. |
| **Graphs** | Distance vs time proves sensing; velocity vs time proves control. |

## 5. If asked “where are the graphs?”

They are generated from real `/obstacle_report` and `/cmd_vel` data using `plot_logger`, or viewed live with `rqt_plot`. See `docs/graphs/` after recording.
