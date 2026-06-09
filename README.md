# Autonomous Warehouse SLAM Explorer

> A ROS 2 Humble + Ignition Fortress simulation of a holonomic mecanum-wheel robot that
> autonomously explores an office / warehouse environment, builds a 3-D map in real time,
> and navigates to goals — all powered by [GenZ-ICP](https://github.com/url-of-genz-icp)
> for LiDAR odometry.

---

## Architecture

```
Velodyne VLP-16 (sim)
        │ /velodyne_points  PointCloud2
        ├──────────────────────────────────► GenZ-ICP
        │                                       │ /odometry  nav_msgs/Odometry
        │                                       ▼
        └──────────────────────────────────► RTAB-Map ──► /map  OccupancyGrid
                                                               │
                                                               ▼
                                                            Nav 2
                                                    (global + local planner)
                                                               │
                                                               ▼
                                                   Frontier Exploration
                                                      (explore_lite)
                                                               │
                                                               ▼
                                              mecanum_kinematics_node
                                            (Twist → per-wheel velocities)
                                                               │
                                                               ▼
                                               ign_ros2_control  /  Ignition Fortress
```

---

## Features

- [x] Holonomic mecanum-wheel drive (full 3-DOF planar motion)
- [x] Velodyne VLP-16 (16-beam, 360°) point cloud in simulation
- [x] GenZ-ICP LiDAR odometry — scan-to-map ICP with planar filtering
- [x] RTAB-Map 3-D SLAM with loop-closure detection
- [x] 2-D occupancy grid published for Nav2 costmaps
- [x] Nav2 autonomous navigation (RegulatedPurePursuit + AMCL)
- [x] Frontier-based autonomous exploration (explore_lite)
- [x] Complex warehouse world (walls, shelf rows, crates, pillars)
- [x] One-command full-demo launch

---

## Prerequisites

| Dependency | Version |
|---|---|
| ROS 2 | Humble |
| Ignition Gazebo | Fortress |
| ros2_control | Humble |
| ign_ros2_control | Humble |
| RTAB-Map ROS | Humble |
| Nav2 | Humble |
| explore_lite | Humble |
| ros_gz_bridge | Humble |

```bash
sudo apt install \
  ros-humble-ign-ros2-control \
  ros-humble-ros-gz-bridge \
  ros-humble-ros-gz-sim \
  ros-humble-rtabmap-ros \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-explore-lite \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher
```

---

## Installation

```bash
# 1 — create a workspace
mkdir -p ~/autonomous_ws/src && cd ~/autonomous_ws/src

# 2 — clone this repo
git clone https://github.com/<your-username>/autonomous-warehouse-slam.git .

# 3 — clone GenZ-ICP (odometry backbone)
git clone https://github.com/<genz-icp-url>.git

# 4 — build
cd ~/autonomous_ws
colcon build --symlink-install

# 5 — source
source install/setup.bash
```

---

## Quick Start

```bash
# Full autonomous demo (sim + SLAM + Nav2 + exploration)
ros2 launch mam_bringup full_demo.launch.py

# Or step-by-step:
ros2 launch mam_simulation sim.launch.py
ros2 launch mam_slam      slam.launch.py
ros2 launch mam_navigation nav.launch.py
ros2 launch mam_exploration explore.launch.py
```

---

## Package Overview

| Package | Role |
|---|---|
| `mam_description` | URDF robot model — mecanum base, VLP-16, RGBD camera, IMU |
| `mam_simulation` | Ignition Fortress warehouse world + robot spawn launch |
| `mam_control` | Mecanum kinematics node + ros2_control controller config |
| `mam_slam` | RTAB-Map config wired to GenZ-ICP odometry |
| `mam_navigation` | Nav2 params tuned for holonomic mecanum robot |
| `mam_exploration` | explore_lite frontier exploration launch |
| `mam_bringup` | Top-level launch that ties everything together |

---

## Acknowledgements

LiDAR odometry powered by **GenZ-ICP**:
> D. Lee, H. Lim, S. Han, *"GenZ-ICP: Generalizable and Degeneracy-Robust ICP-based
> Odometry Estimation"*, IEEE RA-L, 2024.

---

## License

MIT
