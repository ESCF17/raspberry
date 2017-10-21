#!/usr/bin/env python

from beginner_tutorials.srv import * 
import rospy

def reponse_chrono(req):
	rospy.loginfo("Recu");
	if(req.ask == 1):
		return ChronoResponse(rospy.get_time())
	rospy.logerr("Fail");
	return -1

def chrono_serveur():
	rospy.init_node('chrono_serveur');
	s=rospy.Service('srv_chrono',Chrono,reponse_chrono)
	print("j'ecoute")
	rospy.spin()

if __name__== "__main__":
	chrono_serveur()
