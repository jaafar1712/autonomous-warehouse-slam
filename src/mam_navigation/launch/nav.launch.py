import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    nav_pkg  = get_package_share_directory('mam_navigation')
    nav_cfg  = os.path.join(nav_pkg, 'config', 'nav2_params.yaml')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        # 3-D cloud → 2-D LaserScan projection for AMCL / costmaps
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pc2scan',
            remappings=[
                ('cloud_in', '/velodyne_points'),
                ('scan',     '/scan_2d'),
            ],
            parameters=[{
                'use_sim_time': use_sim_time,
                'min_height':   -0.05,
                'max_height':    0.30,
                'range_min':     0.3,
                'range_max':    15.0,
                'angle_increment': 0.00349,  # ~0.2 deg
            }],
        ),

        # Nav2 stack
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            parameters=[nav_cfg, {'use_sim_time': use_sim_time}],
        ),
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            parameters=[nav_cfg, {'use_sim_time': use_sim_time}],
        ),
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[nav_cfg, {'use_sim_time': use_sim_time}],
        ),
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[nav_cfg, {'use_sim_time': use_sim_time}],
        ),
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            parameters=[nav_cfg, {'use_sim_time': use_sim_time}],
        ),
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[nav_cfg, {'use_sim_time': use_sim_time}],
        ),
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[nav_cfg, {'use_sim_time': use_sim_time}],
        ),
    ])
