import rospy
import json
from std_srvs.srv import *
from proximity_processer.srv import *

def pp_init():
    rospy.wait_for_service('proximity_processer/init')
    client = rospy.ServiceProxy('proximity_processer/init', Empty)
    client()

def pp_append():
    rospy.wait_for_service('proximity_processer/append')
    client = rospy.ServiceProxy('proximity_processer/append', Empty)
    client()

def pp_judge():
    rospy.wait_for_service('proximity_processer/judge')
    client = rospy.ServiceProxy('proximity_processer/judge', IsCollision)
    ret = client()
    return ret 

if __name__=='__main__':
    rospy.init_node('tester_pp')

    



