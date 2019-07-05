#!/usr/bin/env python
import rospy
from force_proximity_ros.msg import ProximityStamped
from std_srvs.srv import *
#from proximity_processer.srv import *

class ProxProc:
    def __init__(self):
        sub = rospy.Subscriber("/proximity_sensor", ProximityStamped, self.callback_prox)
        survice_init = rospy.Service("init", Empty, self.handle_request_init)
        survice_append = rospy.Service("append", Empty, self.handle_request_append)
        self.val = None
        self.val_ref = None
        self.val_relative_lst = None

    def handle_request_init(self, req):
        log_str = "proximity processer init " + \
                "with val:" + str(self.val)
        rospy.loginfo(log_str)
        self._init_procedure()
        return EmptyResponse()

    def handle_request_append(self, req):
        val_relative = self.val -self.val_ref
        log_str = "proximity processer append " + \
                "with val:" + str(val_relative)
        rospy.loginfo(log_str)
        self.val_relative_lst.append(val_relative)
        return EmptyResponse()

    def callback_prox(self, data):
        self.val = data.proximity.average

    def _init_procedure(self):
        self.val_ref = self.val
        self.val_relative_lst = [0.0]

if __name__=='__main__':
    rospy.init_node('proxproc', anonymous = True)
    pr = ProxProc()
    rospy.spin()



