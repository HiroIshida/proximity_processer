#!/usr/bin/env python
import rospy
from force_proximity_ros.msg import ProximityStamped
from std_srvs.srv import *
#from proximity_processer.srv import *

class ProxProc:
    def __init__(self):
        sub = rospy.Subscriber("/proximity_sensor", ProximityStamped, self.callback_prox)
        survice_init = rospy.Service("init", Empty, self.handle_request_init)
        self.val = None
        self.val_ref = None

    def handle_request_init(self, req):
        log_str = "proximity processer init " + \
                "with val:" + str(self.val)
        rospy.loginfo(log_str)
        self.val_ref = self.val
        return EmptyResponse()

    def callback_prox(self, data):
        self.val = data.proximity.average

        ref_unset = (self.val_ref is None)
        """
        if ref_unset:
            print "val_ref is not set yet"
        else:
            print self.val - self.val_ref
            """

if __name__=='__main__':
    rospy.init_node('proxproc', anonymous = True)
    pr = ProxProc()
    rospy.spin()



