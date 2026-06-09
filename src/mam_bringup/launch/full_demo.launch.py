"""
Full autonomous warehouse SLAM demo.

Launch order:
  1. Ignition Fortress simulation (warehouse world + robot spawn)
  2. ros2_control spawners + mecanum kinematics node
  3. GenZ-ICP odometry + RTAB-Map SLAM
  4. Nav2 autonomous navigation stack
  5. explore_lite frontier exploration
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def _include(pkg: str, launch_file: str, **kwargs):
    pkg_dir = get_package_share_directory(pkg)
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_dir, 'launch', launch_file)),
        launch_arguments=kwargs.items(),
    )


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        # 1 — Gazebo + robot spawn (t = 0 s)
        _include('mam_simulation', 'sim.launch.py',
                 use_sim_time='true'),

        # 2 — ros2_control + mecanum kinematics (t = 5 s, after Gazebo is up)
        TimerAction(period=5.0, actions=[
            _include('mam_control', 'control.launch.py'),
        ]),

        # 3 — GenZ-ICP + RTAB-Map (t = 8 s, after robot is spawned)
        TimerAction(period=8.0, actions=[
            _include('mam_slam', 'slam.launch.py',
                     use_sim_time='true'),
        ]),

        # 4 — Nav2 (t = 12 s, after SLAM has an initial map)
        TimerAction(period=12.0, actions=[
            _include('mam_navigation', 'nav.launch.py',
                     use_sim_time='true'),
        ]),

        # 5 — Frontier exploration (t = 18 s, after Nav2 lifecycle is active)
        TimerAction(period=18.0, actions=[
            _include('mam_exploration', 'explore.launch.py',
                     use_sim_time='true'),
        ]),
    ])
