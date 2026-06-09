"""
Start slam_toolbox + Nav2 + RViz (Gazebo must already be running).
Usage:
  ros2 launch tb3_slam_nav nav_slam.launch.py
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg         = get_package_share_directory('tb3_slam_nav')
    slam_tb_dir = get_package_share_directory('slam_toolbox')
    nav2_dir    = get_package_share_directory('nav2_bringup')

    slam_params = os.path.join(pkg, 'config', 'slam_toolbox_params.yaml')
    nav2_params = os.path.join(pkg, 'config', 'nav2_params.yaml')
    rviz_config = os.path.join(pkg, 'rviz',   'slam_nav.rviz')

    return LaunchDescription([

        # ── 1. slam_toolbox ──────────────────────────────────────────────────
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(slam_tb_dir, 'launch', 'online_sync_launch.py'),
            ),
            launch_arguments={
                'use_sim_time':     'true',
                'slam_params_file': slam_params,
            }.items(),
        ),

        # ── 2. Nav2 (navigation only, no map_server — slam_toolbox owns /map) ─
        TimerAction(period=3.0, actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(nav2_dir, 'launch', 'navigation_launch.py'),
                ),
                launch_arguments={
                    'use_sim_time': 'true',
                    'params_file':  nav2_params,
                    'autostart':    'true',
                }.items(),
            ),
        ]),

        # ── 3. RViz2 ─────────────────────────────────────────────────────────
        TimerAction(period=2.0, actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                arguments=['-d', rviz_config],
                parameters=[{'use_sim_time': True}],
                output='screen',
            ),
        ]),

        # ── 4. Autonomous waypoint explorer (starts after Nav2 is ready) ─────
        TimerAction(period=15.0, actions=[
            Node(
                package='tb3_slam_nav',
                executable='waypoint_explorer',
                name='waypoint_explorer',
                output='screen',
                parameters=[{'use_sim_time': True}],
            ),
        ]),
    ])
