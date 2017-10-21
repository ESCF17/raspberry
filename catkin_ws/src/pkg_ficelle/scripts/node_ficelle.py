#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy # Permet d'utiliser ROS 
import time
import os
from std_msgs.msg import Int8 # Support du message envoyer dans un topic 


"""
Subscriber : /topic_ficelle_arduino

Roslaunche : ficelle_launcher.xml

Dev : Hugo Pousseur
"""


def callBackFicelle(data):
    if(data.data == 1):
	 rospy.loginfo(rospy.get_caller_id() + 'ENVOIE ROS %s', data.data)
	 os.system("roslaunch pkg_launcher ficelle_launcher.xml")


if __name__ == '__main__':
    try:
	rospy.init_node('node_ficelle', anonymous=True) # Notre noeud on l'initialise 
	rospy.Subscriber('topic_ficelle_arduino', Int8, callBackFicelle)
	rospy.spin()
    except rospy.ROSInterruptException:
        pass
