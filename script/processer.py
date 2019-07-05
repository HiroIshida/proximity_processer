#!/usr/bin/env python
import rospy
from force_proximity_ros.msg import ProximityStamped

class ProxProc:
    def __init__(self):
        self.sub = rospy.Subscriber("/proximity_sensor", ProximityStamped, self.callback_prox)

    def callback_prox(self, data):
        print data.proximity.average

if __name__=='__main__':
    rospy.init_node('listener', anonymous = True)
    pr = ProxProc()
    rospy.spin()



