#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 # impotation sqlite3
#import time # bibliotheque time 
import rospy
import atexit
from std_msgs.msg import String

def send_log():
	#pub = rospy.Publisher('cmd_key_arduino', String, queue_size=10)
	rospy.init_node('node_read_log', anonymous=True) #On initilias le noeud
	pub = rospy.Publisher('cmd_key_arduino',String, queue_size=10) #On lui dit de publier la dedans 
	conn = sqlite3.connect('sauvegarde.db') # Acces à la BDD
	cursor = conn.cursor()
	cursor.execute("""SELECT id_log, char, time FROM LOG""")
	rows = cursor.fetchall()
	conn.close()
	temps_ref= rospy.get_time()
	for row in rows:
	    print('DONNEE BASE DE DONNE {0} : {1} - {2}'.format(row[0], row[1], row[2]))
	    duree = row[2]
	    rospy.loginfo(row[1])
            pub.publish(row[1])
	    temps = time.clock();
            while(temps-temps_ref<duree and not rospy.is_shutdown()):
		    temps = rospy.get_time()
    	            temps_ref = temps;
	            if row[1] == 'c' :
		    	pub.publish(row[1])
		    	exit() 

if __name__ == '__main__':
    try:
       	send_log()
    except rospy.ROSInterruptException:
        pass


