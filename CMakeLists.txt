cmake_minimum_required(VERSION 2.8.3)
project(proximity_processer)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  message_generation
)


add_service_files(
  FILES
  IsCollision.srv
)

add_message_files(
  FILES
  FloatHeader.msg
)



generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs geometry_msgs jsk_recognition_msgs
)
