from classes import *
from djitellopy import Tello
import cv2
import torch
import numpy as np
from PIL import Image

model = torch.hub.load('/Users/andreacasassa/yolov5', 'custom', path='/Users/andreacasassa/yolov5/models/yolov5s.pt', source='local')
classes = getclass()

def intializeTello():
	# CONNECT TO TELLO
	myDrone = Tello()
	myDrone.connect()
	myDrone.for_back_velocity = 0
	myDrone.left_right_velocity = 0
	myDrone.up_down_velocity = 0
	myDrone.yaw_velocity = 0
	myDrone.speed =0
	print(myDrone.get_battery())
	myDrone.streamoff()
	myDrone.streamon()
	return myDrone

def telloGetFrame(myDrone,w=360,h=240):
	# GET THE IMGAE FROM TELLO
	myFrame = myDrone.get_frame_read()
	myFrame = myFrame.frame
	img = cv2.resize(myFrame, (w, h))
	return img

def findFace(img):

	# faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

	#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	results = model(imgGray)

	myFacesListC = []
	myFaceListArea = []

	for res in results.xyxy[0]:

		x, y, w, h, conf, cl = res

		x = int(x)
		y = int(y)
		w = int(w)
		h = int(h)
		conf = float(conf)
		cl = int(cl)

		if cl==0 and conf > 0.60:


	        #Rectangle + associated text
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
			text = "{}: {:.4f}".format(classes[cl], conf)
			cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)

			cx = x + w//2
			cy = y + h//2
			area = w*h
			myFacesListC.append([cx,cy])
			myFaceListArea.append(area)

		else:

			continue

	if len(myFaceListArea) != 0:
		i = myFaceListArea.index(max(myFaceListArea))
		# index of closest face
		return img,[myFacesListC[i],myFaceListArea[i]]
	else:
		return img, [[0,0],0]

def trackFace(myDrone,c,w,pid,pError):
	#print(c)
	error_rotation= c[0][0] - w//2
	speed_rotation = pid[0]*error_rotation + pid[1] * (error_rotation-pError[0])
	speed_rotation = int(np.clip(speed_rotation, -50, 50))

	# error_distance= (c[1] - 10000)/10000*300
	# speed_distance = pid[0]*error_distance + pid[1] * (error_distance-pError[1])
	# speed_distance = -int(np.clip(speed_distance, -30, 30))


	if c[0][0] != 0: # and c[1] != 0:
		myDrone.yaw_velocity = speed_rotation
		#myDrone.for_back_velocity = speed_distance
	else:
		myDrone.left_right_velocity = 0
		myDrone.for_back_velocity = 0
		myDrone.up_down_velocity = 0
		myDrone.yaw_velocity = 0
		error_rotation = 0
		# error_distance= 0

	# SEND VELOCITY VALUES TO TELLO
	if myDrone.send_rc_control:
		myDrone.send_rc_control(myDrone.left_right_velocity,myDrone.for_back_velocity,
		myDrone.up_down_velocity, myDrone.yaw_velocity)

	return [error_rotation, 0]#error_distance]