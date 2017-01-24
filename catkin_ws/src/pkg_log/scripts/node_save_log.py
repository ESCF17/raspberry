#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Les importations nécessitant pour ajouter les valeurs dans la base de donnee
import sqlite3 # impotation sqlite3
import rospy
import time
from std_msgs.msg import String # On récupère les commandes pour les inserer dans la base de données 

#conn = sqlite3.connect('sauvegarde.db')
#c = conn.cursor()


def suppression_tuple():
	conn = sqlite3.connect('sauvegarde.db')
        c = conn.cursor()
	c.execute("DELETE FROM LOG")
        conn.commit()
        conn.close()


def ajout_log_dans_base(char,temps):
	conn = sqlite3.connect('sauvegarde.db')
	c = conn.cursor()
	c.execute("INSERT INTO LOG (char,time) VALUES ('"+char+"',"+str(temps)+")")
	print("INSERTION : "+char+" / "+str(temps));
	conn.commit()
	conn.close()		

def callback(data):
    global chaine_before
    if chaine_before != 'c':
	    chaine = data.data   
	    global TEMPS_REF
	    temps = rospy.get_time()
	    local_ref = TEMPS_REF
	    TEMPS_REF = temps
	    temps = temps - local_ref
	    ajout_log_dans_base(chaine_before,temps)
	    chaine_before = chaine
    else: 
	ajout_log_dans_base(chaine_before,0)
	exit()

	
def listener():
    rospy.init_node('node_save_log', anonymous=True)
    #rospy.loginfo("Enregistrement en cours");
    global TEMPS_REF
    TEMPS_REF = rospy.get_time();
    rospy.Subscriber('cmd_key_arduino', String, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        chaine_before = 'a'
    	temps_ref = 0;
    	suppression_tuple()
   	listener()
    except rospy.ROSInterruptException:
        pass








