#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import pyrosbag
from pkg_log.srv import *

"""
Srv : log_srv

Dev : Hugo Pousseur
"""

def ask_to_server():
    rospy.wait_for_service('log_srv')
    try:
        ask = rospy.ServiceProxy('log_srv', LogSrv) 
        reponse = ask(O) 
        print reponse.data," ",reponse.time
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def ask_to_server_bool(index):
    rospy.wait_for_service('log_bool_srv')
    try:
        ask = rospy.ServiceProxy('log_bool_srv', LogSrvBool) 
        reponse = ask(index) 
        if(reponse.success == 1):
		print "Demande prise en compte"
		rospy.loginfo("Demande prise en compte")
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


if __name__ == "__main__":
    if len(sys.argv) == 2:
        index = int(sys.argv[1])
	ask_to_server_bool(index)
    else:
	ask_to_server(0)
        sys.exit(1)
