#!/usr/bin/python


from rospy import init_node, is_shutdown	
import select, termios,sys,tty
import MySQLdb as mdb	



def getKey():
	tty.setcbreak(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = ord(sys.stdin.read(1))
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

def keyboardToAction(num) :
	result = False 
	global currentY
	global currentX	
	ajout = 20
	if(num == 65) : 
		print "UP"
		currentY -= ajout
		result = True
	elif(num == 66) : 
		print "DOWN" 
		result = True
		currentY += ajout
	elif(num == 68) : 
		print "LEFT"
		result = True
		currentX -= ajout
	elif(num == 67) : 
		print "RIGHT"
		result = True
		currentX += ajout
	return result

def connectionBaseMYSQL():
	conn = mdb.connect('localhost','root','root','test_ros')
	cursor = conn.cursor()
	cursor.execute("""INSERT INTO test_coord (coordX,coordY) VALUES (%s,%s)""",(currentX,currentY))
	conn.commit()
	cursor.close()
	conn.close()


if __name__ == '__main__' : 
	init_node('test_coord_keyboard',anonymous=True)
	settings = termios.tcgetattr(sys.stdin)
	tout_va_bien = True
	currentX = 150
	currentY = 1100
	while not is_shutdown() and tout_va_bien:
		key = getKey()
		if(keyboardToAction(key)):
			connectionBaseMYSQL()
		elif(key == 113):
			tout_va_bien = False	
