#!/usr/bin/env python
import rospy
import tf
from std_msgs.msg import *
import numpy as np
from math import *
from force_proximity_ros.msg import ProximityStamped
from proximity_processer.msg import *

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

class MyQueue:
    def __init__(self, N):
        self.N = N
        self.data = [0 for n in range(N)]

    def push(self, elem):
        tmp = self.data[1:self.N]
        tmp.append(elem)
        self.data = tmp

    def mean(self):
        return sum(self.data)*1.0/self.N

class ProxProc:
    def __init__(self):
        sub = rospy.Subscriber("/proximity_sensor", ProximityStamped, self.callback_prox)
        self.pub = rospy.Publisher('test', FloatHeader, queue_size=1)
        self.t_pre = None
        self.p_pre = None
        self.val = None
        self.val_pre = None

        self.vel_queue = MyQueue(30)
        self.dval_queue = MyQueue(30)

    def callback_prox(self, data):
        self.val = data.proximity.average

    def compute_derivative(self):
        fr_target = 'base_link'
        fr_source = 'l_gripper_tool_frame'
        listener.waitForTransform(fr_target, fr_source, rospy.Time(), rospy.Duration(1.0))
        p, rot = listener.lookupTransform(fr_target, fr_source, rospy.Time(0))
        t = rospy.get_time()

        isInitialized = (self.t_pre is not None)
        if isInitialized:
            dt = t - self.t_pre
            dp = (np.array(p) - np.array(self.p_pre))/dt
            dp_norm = np.linalg.norm(dp)
            self.vel_queue.push(dp_norm)
            vel_average = self.vel_queue.mean()

            dval = (self.val - self.val_pre)/dt
            self.dval_queue.push(dval)
            dval_average = self.dval_queue.mean()

            if vel_average == 0:
                dv_dp = 0.0
            else:
                dv_dp = dval_average/vel_average

            if abs(dv_dp) > 1e+8:
                dv_dp = 0.0

            print dv_dp

            fh = FloatHeader(header = Header(stamp = rospy.Time.now()), 
                    data = Float64(data = dv_dp))
            self.pub.publish(fh)


        self.t_pre = t
        self.p_pre = p
        self.val_pre = self.val

tfp = ProxProc()

while not rospy.is_shutdown():
    tfp.compute_derivative()
    rospy.sleep(0.01)



