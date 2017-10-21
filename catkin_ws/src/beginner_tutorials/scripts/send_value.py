#!/usr/bin/python
import rospy
from std_msgs.msg import Float32




pub = rospy.Publisher('test_ultrason', Float32, queue_size=10)
rospy.init_node('talker_test_ultrason', anonymous=True)
rate = rospy.Rate(1) # 10hz

while not rospy.is_shutdown():
	entree = raw_input("Distance Avant : ");
	try:
	    valeur =  float(entree);	
	    print("[DONE] DONNEE VALIDE : "+ entree);
	    rospy.loginfo(valeur)
            pub.publish(valeur)
            rate.sleep()
	except ValueError:
	    if entree == "exit" : 
		 exit()
	    else :
    	    	 print("[ERROR] PROBLEME DONNEE	"); 
	   
