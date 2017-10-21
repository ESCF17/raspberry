#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy # Pour gérer ROS 
import sys  # Pour gérer les arguments en entrées


from std_msgs.msg import String
from std_msgs.msg import Float32
from pkg_log.srv import *



"""
To do : 
 - Centraliser les contraintes pour faire avancer le robot
 - Intervient au prêt de l'arduino des moteurs grâce à un service 
 - Permet d'interrompre un service

Subscriber : /topic_ultrason
	     /topic_timer


Dev : Hugo Pousseur
"""

### Variable global ###
ENVOYE_ACCEPTE_ULTRASON = True
ENVOYE_ACCEPTE_TIMER = True
LAST_VALUE_DROP = 1
PUB = None



def callBackUltrason(data):
    rospy.loginfo(rospy.get_caller_id() + 'Call Ulrason %s', data.data)
    global ENVOYE_ACCEPTE_ULTRASON
    global DISTANCE_TOLEREE
    global LAST_VALUE_DROP

    ENVOYE_ACCEPTE_ULTRASON = (data.data > DISTANCE_TOLEREE)
    if (not ENVOYE_ACCEPTE_ULTRASON and ENVOYE_ACCEPTE_TIMER):
	rospy.logwarn('Collision imminante')
	LAST_VALUE_DROP = 0
        ask_to_server_bool(0)
    elif(LAST_VALUE_DROP == 0 and ENVOYE_ACCEPTE_ULTRASON and ENVOYE_ACCEPTE_TIMER):
	LAST_VALUE_DROP = 1
        ask_to_server_bool(1)



	

def callBackTimer(data):
    rospy.loginfo(rospy.get_caller_id() + 'Call Timer %s', data.data)
    global ENVOYE_ACCEPTE_TIMER
    global CHRONO
    global LAST_VALUE_DROP

    ENVOYE_ACCEPTE_TIMER = (data.data < CHRONO)
    if (not ENVOYE_ACCEPTE_TIMER and LAST_VALUE_DROP == 1):
	LAST_VALUE_DROP = 0
        ask_to_server_bool(0)
   


def ask_to_server_bool(valeur):
    rospy.wait_for_service('log_bool_srv')
    try:
        ask = rospy.ServiceProxy('log_bool_srv', LogSrvBool) 
        reponse = ask(valeur) 
        #print reponse.data," ",reponse.time
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e



if __name__ == '__main__':
   DISTANCE_TOLEREE = 50 
   CHRONO = 90  


   rospy.init_node('node_cmd', anonymous=True) 
   if(rospy.has_param('~dist')):
	 DISTANCE_TOLEREE = rospy.get_param('~dist')
   if(rospy.has_param('~chrono')):
	 CHRONO = rospy.get_param('~chrono')
  	
   print "Distance ",DISTANCE_TOLEREE," mm | Chrono ",CHRONO," s"
   
   rospy.Subscriber('topic_ultrason', Float32, callBackUltrason)
   rospy.Subscriber('topic_timer', Float32, callBackTimer) 
   rospy.spin()

   


