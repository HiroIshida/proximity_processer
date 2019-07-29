#!/usr/bin/env python
import rospy
import tf
from std_msgs.msg import Float64
import numpy as np
from math import *

def Rx(a):
    ca = cos(a)
    sa = sin(a)
    arr = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]])
    return arr

def Ry(a):
    ca = cos(a)
    sa = sin(a)
    arr = np.array([[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]])
    return arr

def Rz(a):
    ca = cos(a)
    sa = sin(a)
    arr = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    return arr

def rpy_to_mat(r, p, y):
    mat = Rz(y).dot(Ry(p)).dot(Rx(r))
    return mat

rospy.init_node("talker", anonymous=True)
listener = tf.TransformListener()
pub = rospy.Publisher("chatter", Float64, queue_size = 1)
r = rospy.Rate(10)


while not rospy.is_shutdown():
    print "hage"
    #t_now = rospy.get_rostime()
    fr_target = 'base_link'
    fr_source = 'l_gripper_tool_frame'
    listener.waitForTransform(fr_target, fr_source, rospy.Time(), rospy.Duration(4.0))
    trans, rot = listener.lookupTransform(fr_target, fr_source, rospy.Time(0))
    """
    e = tf.transformations.euler_from_quaternion((rot[0], rot[1], rot[2], rot[3]))
    mat = rpy_to_mat(e[0], e[1], e[2])
    """
    print trans


