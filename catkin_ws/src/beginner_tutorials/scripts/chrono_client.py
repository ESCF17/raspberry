#!/usr/bin/env python

import sys
import rospy
import datetime
from beginner_tutorials.srv import *

def chrono_client(choix):
	rospy.wait_for_service('srv_chrono')
	try:
		requete = rospy.ServiceProxy('srv_chrono',Chrono)
		reponse = requete(choix)
		return reponse.heure
	except rospy.ServiceExcepion, e:
		print "probleme lors de l'appelle"

if __name__=="__main__":
	print "parametre demande %s"%sys.argv[1]
	donnee = chrono_client(int(sys.argv[1]))
	print "donnee brute : %s"%donnee
	print "donnee traiee : %s"%datetime.datetime.fromtimestamp(
        int(donnee)
    ).strftime('%Y-%m-%d %H:%M:%S')
