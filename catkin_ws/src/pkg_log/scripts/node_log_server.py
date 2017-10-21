#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rosbag
import rospy
import time

from std_msgs.msg import String
from std_msgs.msg import Float32
from pkg_log.srv import *

"""
To do :
  - Dans une premier temps permet de créer à partir d'un fichier bag 2 tableaux
  - Créer un service serveur permet au CMD d'avoir la main 
  - Permet de simuler le bag en prenant compte des ordres du CMD

Publisher : /topic_cmd_arduino

Srv(client) : log_srv

Dev : Hugo Pousseur
"""

### VARIABLE GLOBAL ###
DATA_TAB = ['a']
TIME_TAB = []
LAST_VALUE_SEND = 'b'
CONTINUER = True
PUB = None
FREQUENCE = 0.01


def afficher_tableau(tab1,tab2):
	for i in range(min(len(tab1),len(tab2))):
		print "[",tab1[i]," ",tab2[i],"]"

def creation_tableau_log():
	"""
		Permet de créer un tableau pour faciiter l'exploitatin à partir d'un fichier bag
	"""
	temps = 0
	temps_envoie = 100*FREQUENCE
	global DATA_TAB
	global TIME_TAB
	bag = rosbag.Bag('/home/hugo/catkin_ws/src/pkg_log/bag/test.bag')
	for topic, msg, t in bag.read_messages(topics=['/topic_cmd_arduino']):
	    #time = float(str(t)[-12:])
	    time = float(str(t))
	    if(temps == 0):
	    	temps = time
	    #print str(msg)[6:]," ","TRAIT",time,"TS",t,(time-temps)/1000000000
	    DATA_TAB.append(str(msg)[6:])
	    TIME_TAB.append((time-temps)/1000000000+temps_envoie);
	bag.close()
	TIME_TAB.append(-1)
	TIME_TAB[0] = temps_envoie
	
	

def handle_log(req):
    """
		C'est le gestionnaire du service il permet de faire le traitement demandé par le client
		ici on utilise le srv : -> LogSrvBool : 
		  					int8 continu
							---
							int8 success
    """
    global DATA_TAB
    global TIME_TAB
    global CONTINUER
    rospy.loginfo(rospy.get_caller_id() + "Continuer Value : %s",(req.continu))
    CONTINUER = (int(req.continu) == 1)
    rospy.logwarn(rospy.get_caller_id() + "Decision : %s",CONTINUER)
    return LogSrvBoolResponse(1)
    	
def log_server():
    s = rospy.Service('log_bool_srv', LogSrvBool, handle_log)
    rospy.logwarn(rospy.get_caller_id() + "Serveur - Service Log en ecoute")

def envoie_arduino(valeur):
    global PUB
    global LAST_VALUE_SEND
    rospy.loginfo("def envoie : %s",valeur)
    PUB.publish(valeur)
    LAST_VALUE_SEND = valeur
    

def simulation():
	"""
		Permet de créer une simuation, à parir des tableaux créer à partir du fichier bag 
	"""
  	global FREQUENCE
	global CONTINUER
	global LAST_VALUE_SEND
	global DATA_TAB
	global TIME_TAB
	#pubErr = rospy.Publisher('topic_erreur', Float32, queue_size=10)
	temps_additionnel = 0
	debut  = rospy.get_time()		
	commande_validee = 0
	encours = debut
	data_err = 0;
	i = 0
	while(i<(len(DATA_TAB)-1)):
	        envoie_arduino(DATA_TAB[i])
		while(encours - debut <= TIME_TAB[i] - (0.6*FREQUENCE)): # La soustraction a été mise en place après une série de teste mettant en evidence un lien entre la perte et la frequence
			 time.sleep(FREQUENCE)
			 if(CONTINUER):
				if(LAST_VALUE_SEND != DATA_TAB[i]):
					envoie_arduino(DATA_TAB[i])
					debut += temps_additionnel
					temps_additionnel = 0
				encours = rospy.get_time()
			 else :
				if(LAST_VALUE_SEND != 'a'): # On evite de bourinner dans le flux
					envoie_arduino('a')
				temps_additionnel +=FREQUENCE
		difference = abs((encours - debut) - TIME_TAB[i]);				
		print difference
		#pubErr.publish(difference)		
		commande_validee += difference
		#pubErr.publish(commande_validee)		
		i+=1
	envoie_arduino('a')
	#pubErr.publish((commande_validee)/(len(DATA_TAB)-1))
	rospy.logwarn("Moyenne erreur : %s | Cumule : %s",(commande_validee)/(len(DATA_TAB)-1),commande_validee)
	exit()	

if __name__ == "__main__":
    creation_tableau_log()
    rospy.init_node('node_log_server')
    PUB = rospy.Publisher('topic_cmd_arduino', String, queue_size=10)
    if(rospy.has_param('~freq')): 
		# La frequence est a définir entre la perte de precision et de la partie calcul 				  
		# + freq augment et plus la precision ets importante mais plus les calculs sont lours 
		# à titre d'exemple à 10^-5 la frequence est telle que la partie service serveur n'est plus exploitable 
	 FREQUENCE = rospy.get_param('~freq')
    afficher_tableau(DATA_TAB,TIME_TAB)
    log_server()	
    simulation()
    rospy.sleep(0.1)
    rospy.spin()
    


