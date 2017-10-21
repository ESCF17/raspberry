#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy # Permet d'utiliser ROS 
from std_msgs.msg import Float32 # Support du message envoyer dans un topic 
from std_msgs.msg import Int8

"""
Publisher : /topic_cmd_arduino_fusee
Subscriber : /topic_timer

dev : Hugo Pousseur
"""
TEMPS_FIN = 10

	
def shutDown():
  print "shutdown time !!"

def send_value():
	rospy.loginfo(1) 
	pub.publish(1)
	
def callBackTime(data):
    global TEMPS_FIN 
    if(data.data >= TEMPS_FIN):
	send_value()
	rospy.signal_shutdown("node_fusee Shutdown")


if __name__ == '__main__':
    try:
	rospy.init_node('node_fusee', anonymous=True) # Notre noeud on l'initialise
	if(rospy.has_param('~temps')):
		TEMPS_FIN = rospy.get_param('~temps')
	
	
        print "TEMPS ",TEMPS_FIN
 	pub = rospy.Publisher('topic_cmd_arduino_fusee', Int8, queue_size=10) # On crée notre noeud qui publie  
	rospy.Subscriber('topic_timer', Float32, callBackTime)
	rospy.spin()
    except rospy.ROSInterruptException:
        pass

