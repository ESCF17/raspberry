#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Les importations nécessitant pour ajouter les valeurs dans la base de donnee
import sqlite3 # impotation sqlite3
import time
#import atexit
import rospy
from std_msgs.msg import String # On récupère les commandes pour les inserer dans la base de données 

"""
Le but de ce script est de suavegarder les mouvements du robots dans une base de donnee
Pour les réutiliser ulterieurment.
réutilisation du principe de LOG pour déplacer le robot
"""




def ajout_log_dans_base(char,temps):
	conn = sqlite3.connect('sauvegarde.db')
	if(type(char) is str and (type(temps) is float or type(temps) is int)):
		c = conn.cursor()
		c.execute("INSERT INTO LOG (char,time) VALUES ('"+char+"',"+str(temps)+")")
		print("INSERTION : "+char+" / "+str(temps));
		conn.commit()
		conn.close()
	else :
		print("PROBLEME TYPE DE DONNEE");

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + ' %s', data.data)
    global chaine_before
    if chaine_before != 'c':
	    chaine = data.data   
	    global temps_ref
	    temps = int(round(time.time() * 1000))
	    local_ref = temps_ref
	    temps_ref = temps
	    temps = temps - local_ref
	    ajout_log_dans_base(chaine_before,temps)
	    chaine_before = chaine
    else : 
	ajout_log_dans_base(chaine_before,0)
	exit()

	
def listener():
    rospy.init_node('listener_key_log', anonymous=True)
    rospy.Subscriber('cmd_key_arduino', String, callback)
    rospy.spin()


if __name__ == '__main__': 
    chaine_before = 'a'
    temps_ref=int(round(time.time() * 1000))
    listener()
    








