import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    slam_pkg = get_package_share_directory('mam_slam')

    use_sim_time  = LaunchConfiguration('use_sim_time', default='true')
    slam_cfg      = os.path.join(slam_pkg, 'config', 'slam_toolbox_params.yaml')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        # ── ICP odometry → odom frame (no GPU required) ───────────────────────
        Node(
            package='rtabmap_odom',
            executable='icp_odometry',
            name='icp_odometry',
            output='screen',
            parameters=[{
                'use_sim_time':                  use_sim_time,
                'frame_id':                      'base_link',
                'odom_frame_id':                 'odom',
                'publish_tf':                    True,
                'approx_sync':                   True,
                'queue_size':                    10,
                'Icp/VoxelSize':                 '0.05',
                'Icp/MaxCorrespondenceDistance':  '0.15',
                'Odom/Strategy':                 '0',
                'Odom/ResetCountdown':            '0',
            }],
            remappings=[
                ('scan',  '/scan'),
                ('odom',  '/odometry'),
            ],
        ),

        # ── slam_toolbox → map frame ──────────────────────────────────────────
        Node(
            package='slam_toolbox',
            executable='sync_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[slam_cfg, {'use_sim_time': use_sim_time}],
        ),
    ])
