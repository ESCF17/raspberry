#!/usr/bin/python
# -*- coding: utf-8 -*-


# Ce script permet de faire une simulation random de valeur 

import time 
import random

import rospy # Permet d'utiliser ROS 
from std_msgs.msg import Int8 # Support du message envoyer dans un topic 

def position_random():
	choix = random.randint(1, 2)	
	if choix == 2 :
		return -1
	else :
		return 1

def publisher():
	pub = rospy.Publisher('topic_ultrason', Int8, queue_size=10) # On crée notre noeud qui publie 
	rospy.init_node('node_chrono', anonymous=False) # Notre noeud on l'initialise 	
	position_depart = 15;
	rate = rospy.Rate(5) # 10hz
	while(not rospy.is_shutdown()):
		position_depart += position_random()
		position_depart = abs(position_depart)
		rospy.loginfo(position_depart) # On la meme dans les logs pour nous vérifier le bon fonctionnement 
        	pub.publish(position_depart) # On publie la valeur 
		rate.sleep()
		


if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
