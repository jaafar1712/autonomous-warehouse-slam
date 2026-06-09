from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    ctrl_pkg = get_package_share_directory('mam_control')

    return LaunchDescription([
        # Spawners run after controller_manager is up (started by sim.launch.py via ign_ros2_control)
        TimerAction(period=5.0, actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
            ),
        ]),
        TimerAction(period=6.0, actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['wheel_velocity_controller', '--controller-manager', '/controller_manager'],
            ),
        ]),
        TimerAction(period=7.0, actions=[
            Node(
                package='mam_control',
                executable='mecanum_kinematics_node',
                name='mecanum_kinematics_node',
                output='screen',
            ),
        ]),
    ])
