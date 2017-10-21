#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 # impotation sqlite3
import time
import rospy
from std_msgs.msg import String

def send_log():
	pub = rospy.Publisher('cmd_key_arduino', String, queue_size=10)
	rospy.init_node('log_key', anonymous=True)
	conn = sqlite3.connect('sauvegarde.db')
	cursor = conn.cursor()
	cursor.execute("""SELECT id_log, char, time FROM LOG""")
	rows = cursor.fetchall()
	conn.close()
	temps_ref=int(round(time.time() * 1000))
	for row in rows:
	    print('DONNEE {0} : {1} - {2}'.format(row[0], row[1], row[2]))
	    duree = int(row[2])
	    rospy.loginfo(str(row[1]))
            pub.publish(str(row[1]))
	    temps = int(round(time.time() * 1000));
	    while(temps-temps_ref<duree):
		temps = int(round(time.time() * 1000));
		time.sleep(0.2)
    	    temps_ref = temps;
	    if row[1] == 'c' :
		exit() 

if __name__ == '__main__':
    try:
        send_log()
    except rospy.ROSInterruptException:
        pass
