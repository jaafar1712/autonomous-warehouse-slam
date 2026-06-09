#!/usr/bin/env python3
"""
Autonomous waypoint explorer for turtlebot3_house world.
Cycles through a set of patrol points, sending Nav2 goals.
"""
import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose


class WaypointExplorer(Node):
    # (x, y, yaw_deg) — starts near spawn (-2.0,-0.5), expands outward
    # turtlebot3_house world: robot spawns in bottom-left room
    WAYPOINTS = [
        (-1.5, -0.5,    0),   # 0.5m forward — first small move
        (-1.5,  0.5,   90),   # turn and go toward doorway
        (-0.5,  0.5,    0),   # into corridor
        ( 0.5,  0.0,    0),   # center of house
        ( 0.5,  1.5,   90),   # top-right room
        (-0.5,  1.5,  180),   # top-left room
        (-1.5,  0.0,  -90),   # back to left corridor
        ( 0.0, -1.5,    0),   # bottom corridor
        ( 1.0, -1.0,   45),   # bottom-right area
        (-2.0, -0.5,  180),   # back to start
    ]

    def __init__(self):
        super().__init__('waypoint_explorer')
        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self._idx  = 0
        self._busy = False
        self._timer = self.create_timer(5.0, self._tick)
        self.get_logger().info('Waypoint explorer ready, waiting for Nav2…')

    # ── helpers ──────────────────────────────────────────────────────────────

    def _tick(self):
        if self._busy:
            return
        if not self._client.wait_for_server(timeout_sec=1.0):
            self.get_logger().warn('navigate_to_pose action server not ready yet…')
            return
        wp = self.WAYPOINTS[self._idx % len(self.WAYPOINTS)]
        self._send_goal(*wp)

    def _send_goal(self, x, y, yaw_deg):
        yaw = math.radians(yaw_deg)
        goal_msg = NavigateToPose.Goal()
        p = goal_msg.pose
        p.header.frame_id = 'map'
        p.header.stamp.sec = 0       # 0 = use latest available TF, avoids sim_time mismatch
        p.header.stamp.nanosec = 0
        p.pose.position.x = float(x)
        p.pose.position.y = float(y)
        p.pose.orientation.z = math.sin(yaw / 2.0)
        p.pose.orientation.w = math.cos(yaw / 2.0)

        self._busy = True
        self.get_logger().info(
            f'→ waypoint {self._idx % len(self.WAYPOINTS)}: '
            f'({x:.1f}, {y:.1f}, {yaw_deg}°)'
        )
        fut = self._client.send_goal_async(goal_msg)
        fut.add_done_callback(self._on_goal_accepted)

    def _on_goal_accepted(self, future):
        handle = future.result()
        if not handle.accepted:
            self.get_logger().warn('Goal rejected — skipping')
            self._busy = False
            self._idx += 1
            return
        handle.get_result_async().add_done_callback(self._on_goal_done)

    def _on_goal_done(self, future):
        self._idx += 1
        self._busy = False
        self.get_logger().info('Goal reached, moving to next waypoint')


def main():
    rclpy.init()
    node = WaypointExplorer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
