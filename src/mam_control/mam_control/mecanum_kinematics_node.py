#!/usr/bin/env python3
"""
Mecanum-wheel inverse kinematics.

Subscribes to  /cmd_vel  (geometry_msgs/Twist)
Publishes to   /wheel_velocity_controller/commands  (std_msgs/Float64MultiArray)
               order: [FL, FR, RL, RR]

Mecanum X-configuration inverse kinematics:
  ω_FL = (1/r)( vx - vy - (lx+ly)·ωz )
  ω_FR = (1/r)( vx + vy + (lx+ly)·ωz )
  ω_RL = (1/r)( vx + vy - (lx+ly)·ωz )
  ω_RR = (1/r)( vx - vy + (lx+ly)·ωz )
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray


class MecanumKinematicsNode(Node):
    def __init__(self):
        super().__init__('mecanum_kinematics_node')

        self.declare_parameter('wheel_radius', 0.05)   # m
        self.declare_parameter('lx',           0.105)  # half wheelbase (front-rear)
        self.declare_parameter('ly',           0.145)  # half track width (left-right)

        self.r  = self.get_parameter('wheel_radius').value
        self.lx = self.get_parameter('lx').value
        self.ly = self.get_parameter('ly').value

        self.sub = self.create_subscription(
            Twist, '/cmd_vel', self._on_cmd_vel, 10)
        self.pub = self.create_publisher(
            Float64MultiArray, '/wheel_velocity_controller/commands', 10)

        self.get_logger().info(
            f'Mecanum kinematics ready  r={self.r}  lx={self.lx}  ly={self.ly}')

    def _on_cmd_vel(self, msg: Twist):
        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z
        r  = self.r
        l  = self.lx + self.ly

        fl = (vx - vy - l * wz) / r
        fr = (vx + vy + l * wz) / r
        rl = (vx + vy - l * wz) / r
        rr = (vx - vy + l * wz) / r

        out = Float64MultiArray()
        out.data = [fl, fr, rl, rr]
        self.pub.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = MecanumKinematicsNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
