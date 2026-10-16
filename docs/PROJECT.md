# Development of a Virtual Autonomous Robot using ROS2 and Gazebo

## Project objective

Build an **autonomous obstacle detection and avoiding robot** using:

- **Linux** — Ubuntu 22.04 LTS  
- **ROS 2** — Humble Hawksbill  
- **Gazebo** — Classic simulator with lidar and differential drive  

## What was implemented

1. **Ubuntu + ROS 2 + Gazebo integration** via Docker (`tiryoh/ros2-desktop-vnc:humble`) or native Ubuntu 22.04 install.  
2. **Virtual robot** — URDF model, diff-drive plugin, 360° lidar in Gazebo.  
3. **Obstacle detection** — `obstacle_detector` processes `/scan` and publishes sector ranges on `/obstacle_report`.  
4. **Obstacle avoidance** — `obstacle_avoider` publishes `/cmd_vel` (forward, slow, turn, reverse) to steer around obstacles.  
5. **Single launch** — `ros2 launch virtual_robot_bringup bringup.launch.py` starts simulation and autonomy.

## How to run

See [README.md](../README.md):

```bash
docker compose up --build
# Browser: http://127.0.0.1:6080/  (password: ubuntu)
source /home/ubuntu/workspace/install/setup.bash
ros2 launch virtual_robot_bringup bringup.launch.py
```

## Software stack

| Layer | Component |
|-------|-----------|
| OS | Ubuntu 22.04 (Jammy) |
| Middleware | ROS 2 Humble |
| Simulation | Gazebo + `gazebo_ros` |
| Sensing | Lidar (`sensor_msgs/LaserScan`) |
| Actuation | Diff drive (`geometry_msgs/Twist` on `/cmd_vel`) |

## Packages

- `virtual_robot_description` — robot and world  
- `virtual_robot_msgs` — `ObstacleReport`  
- `obstacle_avoidance` — detector and avoider nodes  
- `virtual_robot_bringup` — launch files  
