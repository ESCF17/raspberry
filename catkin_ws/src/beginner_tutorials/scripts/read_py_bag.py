	#!/usr/bin/env python
	import rosbag


	def afficher_tableau(tab1,tab2):
		for i in range(min(len(tab1),len(tab2))):
			print "[",tab1[i]," ",tab2[i],"]"

	temps = 0;
	data_tab = ['a'];
	time_tab = [];

	bag = rosbag.Bag('../../pkg_log/bag/2017-03-02-09-57-07.bag')
	for topic, msg, t in bag.read_messages(topics=['topic_key']):
	    time= float(str(t)[-11:])/1000000000
	    if(temps == 0):
		temps = time
	    print str(msg)[6:]," ",(time-temps)
	    data_tab.append(str(msg)[6:])
	    time_tab.append(time-temps);
	    temps = time
	bag.close()

	time_tab.append(-1)
	time_tab.pop(0)
	data_tab.pop(0)

	#afficher_tableau(data_tab,time_tab)







