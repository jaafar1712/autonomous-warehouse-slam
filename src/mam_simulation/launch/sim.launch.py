import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    desc_pkg = get_package_share_directory('mam_description')
    sim_pkg  = get_package_share_directory('mam_simulation')

    urdf_file  = os.path.join(desc_pkg, 'urdf', 'robot.urdf')
    world_file = os.path.join(sim_pkg,  'worlds', 'warehouse.sdf')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Process URDF through xacro so $(find ...) substitutions are resolved
    robot_description = Command(['xacro ', urdf_file])

    # IGN_GAZEBO_SYSTEM_PLUGIN_PATH: exposes ign_ros2_control plugin to Ignition's loader
    # No software-GL env needed: CPU lidar sensor does not use the render engine
    ign_env = {
        'IGN_GAZEBO_SYSTEM_PLUGIN_PATH': '/opt/ros/humble/lib',
    }

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        # Ignition Gazebo — server-only (-s), no GUI window needed
        ExecuteProcess(
            cmd=['ign', 'gazebo', '-s', '-r', world_file],
            output='screen',
            additional_env=ign_env,
        ),

        # robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': use_sim_time,
            }],
        ),

        # Spawn robot into Ignition (slight delay so world loads first)
        TimerAction(period=2.0, actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-name', 'mam_robot',
                    '-topic', '/robot_description',
                    '-x', '0', '-y', '0', '-z', '0.1',
                ],
                output='screen',
            ),
        ]),

        # ros_gz_bridge — sensor topics Ignition → ROS 2
        TimerAction(period=3.0, actions=[
            Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                name='gz_bridge',
                arguments=[
                    '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
                    '/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU',
                    '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
                ],
                output='screen',
            ),
        ]),
    ])
