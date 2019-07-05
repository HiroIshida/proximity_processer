import rospy
import json
from std_srvs.srv import *
from proximity_processer.srv import *

def pp_init():
    rospy.wait_for_service('init')
    client = rospy.ServiceProxy('init', Empty)
    client()

def pp_append():
    rospy.wait_for_service('append')
    client = rospy.ServiceProxy('append', Empty)
    client()

def pp_judge():
    rospy.wait_for_service('judge')
    client = rospy.ServiceProxy('judge', IsCollision)
    ret = client()
    return ret 

if __name__=='__main__':
    rospy.init_node('tester_pp')

    



