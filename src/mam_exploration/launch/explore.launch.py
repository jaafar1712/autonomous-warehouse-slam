from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        Node(
            package='explore_lite',
            executable='explore',
            name='explore',
            output='screen',
            parameters=[{
                'use_sim_time':         use_sim_time,
                'robot_base_frame':     'base_link',
                'costmap_topic':        'global_costmap/costmap',
                'costmap_updates_topic':'global_costmap/costmap_updates',
                'visualize':            True,
                'planner_frequency':    0.33,
                'progress_timeout':     30.0,
                'potential_scale':      3.0,
                'orientation_scale':    0.0,
                'gain_scale':           1.0,
                'transform_tolerance':  0.3,
                'min_frontier_size':    0.20,
            }],
        ),
    ])
