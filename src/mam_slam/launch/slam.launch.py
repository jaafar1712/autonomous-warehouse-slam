import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    slam_pkg = get_package_share_directory('mam_slam')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    rtabmap_cfg  = os.path.join(slam_pkg, 'config', 'rtabmap.yaml')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        # ── GenZ-ICP odometry ───────────────────────────────────────────────
        Node(
            package='genz_icp',
            executable='odometry_node',
            name='genz_icp_odometry',
            output='screen',
            parameters=[{
                'use_sim_time':   use_sim_time,
                'odom_frame':     'odom',
                'base_frame':     'base_link',
                'publish_odom_tf': True,
                'deskew':         False,
                'max_range':      50.0,
                'min_range':      0.3,
                'voxel_size':     0.1,
                'map_cleanup_radius': 50.0,
                'desired_num_voxelized_points': 1000,
                'planarity_threshold':          0.2,
                'max_points_per_voxel':         1,
                'max_num_iterations':           100,
                'convergence_criterion':        0.0001,
                'initial_threshold':            2.0,
                'min_motion_th':                0.05,
                'visualize':                    False,
            }],
            remappings=[('pointcloud_topic', '/velodyne_points')],
        ),

        # ── RTAB-Map SLAM ────────────────────────────────────────────────────
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[rtabmap_cfg, {'use_sim_time': use_sim_time}],
            remappings=[
                ('odom',         '/odometry'),
                ('scan_cloud',   '/velodyne_points'),
                ('grid_map',     '/map'),
            ],
            arguments=['--delete_db_on_start'],
        ),

        # ── RTAB-Map visualisation (optional RViz-compatible pointcloud map) ─
        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            name='rtabmap_viz',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            remappings=[
                ('odom',       '/odometry'),
                ('scan_cloud', '/velodyne_points'),
            ],
        ),
    ])
