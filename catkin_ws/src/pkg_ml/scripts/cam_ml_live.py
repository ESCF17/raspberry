#!/usr/bin/env python

import os
import sys
import click
import cv2

import rospy
from std_msgs.msg import Int16


DEFAULT_CASCADE_FOLDER = 'ref_cascade'
DEFAULT_FRONTAL_FACE_CLASSIFIER = 'haarcascade_frontalface_default.xml'
DEFAULT_EYE_CLASSIFIER = 'haarcascade_eye.xml'


def add_eyes_rect(gray, frame, eye_cascade, x, y, w, h):
    eye_gray = gray[y:y + h, x:x + w]
    eye_color = frame[y:y + h, x:x + w]
    eyes_data = eye_cascade.detectMultiScale(eye_gray)

    for (ex, ey, ew, eh) in eyes_data:
        cv2.rectangle(img=eye_color,
                      pt1=(ex, ey),
                      pt2=(ex + ew, ey + eh),
                      color=(255, 255, 0),
                      thickness=2)

    eyes_text = '{} eye'.format(len(eyes_data)) if len(
        eyes_data) == 1 else '{} eyes'.format(len(eyes_data))
    return ' - ' + eyes_text

def positionToAngle(width,value):
	return 180/width*value


def main(): 

    pubHori = rospy.Publisher('topic_angle_hori', Int16, queue_size=10)
    pubVert = rospy.Publisher('topic_angle_vert', Int16, queue_size=10)

    rospy.init_node('node_angle', anonymous=True)
    
    # Define cascade classifiers
    face_cascade = cv2.CascadeClassifier(DEFAULT_CASCADE_FOLDER+'/'+DEFAULT_FRONTAL_FACE_CLASSIFIER)
    eye_cascade = cv2.CascadeClassifier(DEFAULT_CASCADE_FOLDER+'/'+DEFAULT_EYE_CLASSIFIER)
    eyes = True
    video_capture = cv2.VideoCapture(0)
    
    width_capture_video = video_capture.get(3)
    height_capture_video = video_capture.get(4)

    face_text = ""
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_data = face_cascade.detectMultiScale(gray, 1.2, 5)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces_data:
            cv2.rectangle(img=frame,
                          pt1=(x, y),
                          pt2=(x + w, y + h),
                          color=(255, 0, 0),
                          thickness=2)
	    cv2.line(frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 255), thickness=1, lineType=4, shift=0)
	    cv2.line(frame, pt1=(x, y+h), pt2=(x+w, y), color=(255, 0, 255), thickness=1, lineType=4, shift=0)
            cv2.putText(img=frame,
                    text="Position X : "+str(x)+" Y : "+str(y),
                    org=(x, y+h+10),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.4,
                    color=(0,255,255))	

            face_text = '{} face'.format(len(faces_data)) if len(
                faces_data) == 1 else '{} faces'.format(len(faces_data))
            (x+w/2)
	    
	    position_x = x #+w/2  
            position_y = y

	    rospy.loginfo("Data angle hori: %d",positionToAngle(width_capture_video,position_x))
	    rospy.loginfo("Data angle vert: %d",positionToAngle(height_capture_video,position_y))
            pubHori.publish(180-positionToAngle(width_capture_video,position_x))
            pubVert.publish(30+positionToAngle(height_capture_video,position_y))

            # If we want to see the eyes
            if eyes:
                face_text += add_eyes_rect(gray,
                                           frame,
                                           eye_cascade,
                                           x, y, w, h)
	
        # Display the number of faces detected
        cv2.putText(img=frame,
                    text="DaVinciBot",
                    org=(10, 30),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.3,
                    color=(30,30,30))

	cv2.putText(img=frame,
                    text=face_text,
                    org=(10, 50),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.3,
                    color=(30,30,30))

        # Display the resulting frame
        cv2.imshow('Face Detection using a webcam ', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


