#!/usr/bin/python


from rospy import init_node, is_shutdown
import MySQLdb as mdb	
import select, termios,sys,tty



def getKey():
	tty.setcbreak(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = ord(sys.stdin.read(1))
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

def keyboardToAction(num) :
	result = False 
	if(num == 65) : 
		print "UP"
		result = True
	elif(num == 66) : 
		print "DOWN" 
		result = True
	elif(num == 68) : 
		print "LEFT"
		result = True
	elif(num == 67) : 
		print "RIGHT"
		result = True
	return result


if __name__ == '__main__' : 
	init_node('test_keyboard',anonymous=True)
	settings = termios.tcgetattr(sys.stdin)
	tout_va_bien = True
	while not is_shutdown() and tout_va_bien:
		key = getKey()
		if(keyboardToAction(key)):
			a=2
		elif(key == 113):
			tout_va_bien = False	
