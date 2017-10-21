#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rosbag
import rospy
from pkg_log.srv import *


DATA_TAB = ['']
TIME_TAB = []

def afficher_tableau(tab1,tab2):
	for i in range(min(len(tab1),len(tab2))):
		print "[",tab1[i]," ",tab2[i],"]"

def creation_tableau_log():
	temps = 0
	global DATA_TAB
	global TIME_TAB
	bag = rosbag.Bag('/home/hugo/catkin_ws/src/pkg_log/bag/2017-03-02-09-57-07.bag')
	for topic, msg, t in bag.read_messages(topics=['topic_key']):
	    time= float(str(t)[-11:])/1000000000
	    if(temps == 0):
		temps = time
	    print str(msg)[6:]," ",(time-temps)
	    DATA_TAB.append(str(msg)[6:])
	    TIME_TAB.append(time-temps);
	    temps = time
	bag.close()
	TIME_TAB.append(-1)
	TIME_TAB.pop(0)
	DATA_TAB.pop(0)

def ask_to_server(index):
    rospy.wait_for_service('log_srv')
    try:
        ask = rospy.ServiceProxy('log_srv', LogSrv) 
        reponse = ask(index) 
        print reponse.data," ",reponse.time
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def handle_log(req):
    global DATA_TAB
    global TIME_TAB
    rospy.loginfo(rospy.get_caller_id() + "Index a retourner : %s",(req.index))
    return LogSrvResponse(DATA_TAB[req.index],TIME_TAB[req.index])

def log_server():
    rospy.init_node('node_log_server')
    s = rospy.Service('log_srv', LogSrv, handle_log)
    rospy.loginfo(rospy.get_caller_id() + "Serveur - Service Log en ecoute")
    rospy.spin()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        index = int(sys.argv[1])
	ask_to_server(index)
    else:
        sys.exit(1)

#afficher_tableau(data_tab,time_tab)
