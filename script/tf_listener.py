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

class tf_processer:
    def __init__(self):
        self.t_pre = None
        self.p_pre = None

    def compute_derivative(self):
        fr_target = 'base_link'
        fr_source = 'l_gripper_tool_frame'
        listener.waitForTransform(fr_target, fr_source, rospy.Time(), rospy.Duration(4.0))
        p, rot = listener.lookupTransform(fr_target, fr_source, rospy.Time(0))
        t = rospy.get_time()

        isInitialized = (self.t_pre is not None)
        if isInitialized:
            dt = t - self.t_pre
            dp = (np.array(p) - np.array(self.p_pre))/dt
            vel = np.linalg.norm(dp)
            print vel

        self.t_pre = t
        self.p_pre = p

tfp = tf_processer()

while not rospy.is_shutdown():
    tfp.compute_derivative()
    rospy.sleep(0.03)



