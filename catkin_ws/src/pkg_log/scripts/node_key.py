#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sys, select, termios, tty

msg = """
Controle du Robot par SSH
Developper par DaVinciBot and Co 
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
CUT MOTEUR  |    c
------------------
"""


avancement={
	'z','s','q','d','a',
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
	return chaine
	


if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	pub = rospy.Publisher('cmd_key_arduino', String, queue_size = 1)
	rospy.init_node('node_key',anonymous=True)
	caMarche = 1
	print(msg)
	try:
		while caMarche:
			key = getKey()
			if key in avancement:
				print(keyToChaine(key))	
				pub.publish(key)		
			elif(key=='c') :
				print("ON ARRETE LES MOTEURS")
				pub.publish(key)		
				caMarche = 0
			
	except rospy.ROSInterruptException:
        	pass



