#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32

def callback(data):
    temps = data.data
    rospy.loginfo(rospy.get_caller_id() + "distance = ", temps)
    #here update your label, I assume the following (maybe not correct)
    v = StringVar()
    v.set(temps)
    self.clock = Label(frame, font=('times', 20, 'bold'), bg='green', textvariable = v)
    self.clock.pack(fill=BOTH, expand=1)

def listener():
    rospy.init_node('node_tk_timer', anonymous=True)
    rospy.Subscriber("topic_timer", Float32, callback)  
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
