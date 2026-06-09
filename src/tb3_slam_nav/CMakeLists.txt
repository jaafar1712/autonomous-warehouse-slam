cmake_minimum_required(VERSION 3.8)
project(tb3_slam_nav)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

install(PROGRAMS
  scripts/waypoint_explorer.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME waypoint_explorer
)

install(DIRECTORY launch config rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
