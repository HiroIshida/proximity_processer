#!/usr/bin/env python
import rospy
from force_proximity_ros.msg import ProximityStamped
from std_srvs.srv import *
#from proximity_processer.srv import *

class ProxProc:
    threshold = 500

    def __init__(self):
        sub = rospy.Subscriber("/proximity_sensor", ProximityStamped, self.callback_prox)
        survice_init = rospy.Service("init", Empty, self.handle_request_init)
        survice_append = rospy.Service("append", Empty, self.handle_request_append)
        survice_judge = rospy.Service("judge", Empty, self.handle_request_judge)
        self.val = None
        self.val_ref = None
        self.val_relative_lst = []

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

    def handle_request_judge(self, req):
        print self._isCollision()
        return EmptyResponse()

    def callback_prox(self, data):
        self.val = data.proximity.average

    def _init_procedure(self):
        self.val_ref = self.val
        self.val_relative_lst = [0.0]

    def _isCollision(self):
        valr0 = self.val_relative_lst[-1] 
        if valr0 < self.threshold:
            rospy.loginfo("below the threshold")
            return False
        if len(self.val_relative_lst) < 3:
            rospy.loginfo("to judge, at least 3 vals are required")
            return False  
        valr1 = self.val_relative_lst[-2] 
        valr2 = self.val_relative_lst[-3] 
        dif0 = valr0 - valr1 
        dif1 = valr1 - valr2
        rospy.loginfo("compare")
        boolean = (dif0 < dif1)
        return boolean


if __name__=='__main__':
    rospy.init_node('proxproc', anonymous = True)
    pr = ProxProc()
    rospy.spin()



