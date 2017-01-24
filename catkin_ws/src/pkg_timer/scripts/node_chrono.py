#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Permet de crer un chonometre qui publie pour aider les différents noeuds au fonctionnement

import rospy # Permet d'utiliser ROS 
from std_msgs.msg import Float32 # Support du message envoyer dans un topic 




def chronometre():
    pub = rospy.Publisher('time', Float32, queue_size=10) # On crée notre noeud qui publie 
    rospy.init_node('node_chrono', anonymous=False) # Notre noeud on l'initialise 
    rate = rospy.Rate(5) # 10hz
    debut = rospy.get_time() # Notre référence 
    temps = 0; # Notre chrono
    while not rospy.is_shutdown() and temps < 90:
        temps = rospy.get_time() - debut # Diff = chrono
	rospy.loginfo(temps) # On la meme dans les logs pour nous vérifier le bon fonctionnement 
        pub.publish(temps) # On publie la valeur 
        rate.sleep() # On met un rate de de 10hz pour éviter une sur consommation inutile  


if __name__ == '__main__':
    try:
        chronometre()
    except rospy.ROSInterruptException:
        pass

