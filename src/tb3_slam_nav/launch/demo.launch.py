"""
TurtleBot3 Burger Cam — autonomous SLAM + Nav2 demo
====================================================
Starts in order:
  t=0s   Gazebo Classic 11 (turtlebot3_house world, burger_cam robot)
  t=3s   RViz2 (map + scan + camera + nav2 paths)
  t=5s   slam_toolbox online_sync
  t=8s   Nav2 navigation stack
  t=20s  Waypoint explorer (autonomous patrol)

Map saving:
  ros2 run nav2_map_server map_saver_cli -f ~/map
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg          = get_package_share_directory('tb3_slam_nav')
    tb3_gz_dir   = get_package_share_directory('turtlebot3_gazebo')
    slam_tb_dir  = get_package_share_directory('slam_toolbox')
    nav2_dir     = get_package_share_directory('nav2_bringup')

    slam_params  = os.path.join(pkg, 'config', 'slam_toolbox_params.yaml')
    nav2_params  = os.path.join(pkg, 'config', 'nav2_params.yaml')
    rviz_config  = os.path.join(pkg, 'rviz',   'slam_nav.rviz')

    return LaunchDescription([
        # ── Environment ──────────────────────────────────────────────────────
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger_cam'),
        SetEnvironmentVariable(
            'GAZEBO_MODEL_PATH',
            '/opt/ros/humble/share/turtlebot3_gazebo/models',
        ),

        # ── Gazebo Classic 11 + turtlebot3_house ─────────────────────────────
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3_gz_dir, 'launch', 'turtlebot3_house.launch.py'),
            ),
            launch_arguments={
                'x_pose': '-2.0',
                'y_pose': '-0.5',
            }.items(),
        ),

        # ── RViz2 ─────────────────────────────────────────────────────────────
        TimerAction(period=3.0, actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                arguments=['-d', rviz_config],
                parameters=[{'use_sim_time': True}],
                output='screen',
            ),
        ]),

        # ── slam_toolbox ──────────────────────────────────────────────────────
        TimerAction(period=5.0, actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(slam_tb_dir, 'launch', 'online_sync_launch.py'),
                ),
                launch_arguments={
                    'use_sim_time':     'true',
                    'slam_params_file': slam_params,
                }.items(),
            ),
        ]),

        # ── Nav2 ──────────────────────────────────────────────────────────────
        TimerAction(period=8.0, actions=[
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

        # ── Autonomous waypoint explorer ──────────────────────────────────────
        TimerAction(period=20.0, actions=[
            Node(
                package='tb3_slam_nav',
                executable='waypoint_explorer',
                name='waypoint_explorer',
                output='screen',
                parameters=[{'use_sim_time': True}],
            ),
        ]),
    ])
