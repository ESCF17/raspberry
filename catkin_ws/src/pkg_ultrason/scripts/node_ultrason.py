#!/usr/bin/python
# -*- coding: utf-8 -*-

import time 
import random
import rospy # Permet d'utiliser ROS 
from std_msgs.msg import Float32 # Support du message envoyer dans un topic 
from std_msgs.msg import String

"""
Subscriber : /topic_ultrason_arduino
Publisher : /topic_ultrason 

dev : Hugo Pousseur
"""

### Variable global ####
PUB = None
RATE = None


def publisher(distance):
	global PUB
	global RATE
	rospy.loginfo(float(distance)) # On la meme dans les logs pour nous vérifier le bon fonctionnement 
        pub.publish(float(distance)) # On publie la valeur 
	rate.sleep()
		

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'Valeur brute ultrason %s', data.data)
    splitPosition = (data.data).index('S')
    distanceN = (data.data)[1:splitPosition]
    distanceS = (data.data)[splitPosition+1:]
    publisher(distanceN)
    publisher(distanceS)
    	

def listener():
    rospy.Subscriber('topic_ultrason_arduino', String, callback)  
    rospy.spin()


if __name__ == '__main__':
    try:
	rospy.init_node('node_ultrason', anonymous=True) # Notre noeud on l'initialise 
	pub = rospy.Publisher('topic_ultrason', Float32, queue_size=10)
	rate = rospy.Rate(5) # 10hz
        listener()
	
    except rospy.ROSInterruptException:
        pass
