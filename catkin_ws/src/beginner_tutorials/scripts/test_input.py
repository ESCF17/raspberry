#!/usr/bin/python


from rospy import init_node, is_shutdown

if __name__ == '__main__' : 
	init_node('input_test',anonymous=True)
	while not is_shutdown():
		print "Dites moi tout  : "
		qqchose = raw_input()
		print "ok je prends note "+qqchose


