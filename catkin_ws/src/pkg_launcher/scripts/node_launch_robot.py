#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy # Permet d'utiliser ROS 
import time
import os
from std_msgs.msg import Int8 # Support du message envoyer dans un topic 


def publisher():
    	pub = rospy.Publisher('topic_launcher', Int8, queue_size=10) # On crée notre noeud qui publie 
	rospy.init_node('node_launcher', anonymous=False) # Notre noeud on l'initialise 
	time.sleep(3)
	print "GO GO GO"	
	rospy.loginfo(1) # On la meme dans les logs pour nous vérifier le bon fonctionnement 
        pub.publish(1) # On publie la valeur 
        


if __name__ == '__main__':
    try:
        #publisher()
	os.system("roslaunch pkg_launcher ficelle_launcher.xml")
    except rospy.ROSInterruptException:
        pass
