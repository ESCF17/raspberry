#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

import sys, select, termios, tty


"""
Publisher : /topic_cmd_arduino

dev : Hugo Pousseur
"""

msg = """
Controle du Robot par SSH

---- Commandes ----
Avancer     |    z
-------------------
Reculer     |    s
-------------------
Droit       |    d
-------------------
Gauche      |    q
-------------------
STOPPER     |    a
-------------------
STOP PROCC  |    c
-------------------
TAPIS UP    |    +
-------------------
TAPIS DOWN  |    -
-------------------
"""


avancement={
	'z','s','q','d','a'
}

tapis={
	'-','+'
}

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def keyToChaine(caractere):
	chaine = "[LOG MOVE]["+caractere +"] Le Robot "
	if(caractere=='z'):
		chaine += "AVANCE"
	elif(caractere=='s'):
		chaine += "RECULE"
	elif(caractere=='q'):
		chaine +="TOURNE A GAUCHE"
	elif(caractere=='d'):
		chaine +="TOURNE A DROITE"
	elif(caractere=='a'):
		chaine +="S'ARRETE"
	elif(caractere=='+'):
		chaine +="Ca monte"
	elif(caractere=='-'):
		chaine +="Ca descencd"
	return chaine


if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	pub = rospy.Publisher('topic_cmd_arduino', String, queue_size = 1)
	pubTapis = rospy.Publisher('topic_tapis', Int8, queue_size = 1)
	rospy.init_node('node_key',anonymous=True)
	date_last_send = rospy.get_time()
	caMarche = 1
	print(msg)
	try:
		while caMarche:
			key = getKey()
			if key in avancement and rospy.get_time() - date_last_send > 0.5:
				print(keyToChaine(key))
				date_last_send = rospy.get_time()	
				pub.publish(key)	
			elif key in tapis:
				print(keyToChaine(key))
				if(key=='+'):
					pubTapis.publish(12)
				elif(key=='-'):
					pubTapis.publish(11)	
			elif(key=='c') :
				print("ON ARRETE LES MOTEURS")
				pub.publish('a')		
				caMarche = 0
			
	except rospy.ROSInterruptException:
        	pass



