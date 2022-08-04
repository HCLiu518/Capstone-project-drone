from djitellopy import Tello
import cv2
import numpy as np

def intializeTello():
	# CONNECT TO TELLO
	myDrone = Tello()
	myDrone.connect()
	myDrone.for_back_velocity = 0
	myDrone.left_right_velocity = 0
	myDrone.up_down_velocity = 0
	myDrone.yaw_velocity = 0
	myDrone.speed =0
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
	faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces, rejectLevels, levelWeights = faceCascade.detectMultiScale3(imgGray, 1.1, 4, outputRejectLevels=True)

	myFacesListC = []
	myFaceListArea = []
	myFaceConf = []

	for ((x, y, w, h), _, lw) in zip(faces, rejectLevels, levelWeights):
		cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
		cx = x + w//2
		cy = y + h//2
		area = w*h
		myFacesListC.append([cx,cy])
		myFaceListArea.append(area)
		myFaceConf.append(lw)
		#print(area)

	if len(myFaceListArea) != 0:
		i = myFaceListArea.index(max(myFaceListArea))
		# index of closest face
		return img,[myFacesListC[i],myFaceListArea[i],myFaceConf[i]]
	else:
		return img, [[0,0],0,0]

def trackFace(myDrone,c,w,h,area,pid,pError):
	#print(c)
	## Rotation
	error_rotation= (c[0][0] - w//2)
	speed_rotation = pid[0]*error_rotation + pid[1] * (error_rotation-pError[0])
	speed_rotation = int(np.clip(speed_rotation, -100, 100))

	## Distance
	if abs(c[1] - area) >= area//2:
		error_distance= (abs(c[1] - area))**0.5
		speed_distance = pid[2]*error_distance + pid[3] * (error_distance-pError[1])
		if c[1] - area >= 0:
			speed_distance = -int(np.clip(speed_distance, -50, 50))
		else:
			speed_distance = int(np.clip(speed_distance, -50, 50))
	else:
		error_distance = 0
		speed_distance = 0

	## Height
	error_height= (c[0][1] - h//2)
	speed_height = pid[0]*error_height + pid[1] * (error_height-pError[2])
	speed_height = -int(np.clip(speed_height, -100, 100))

	if c[0][0] != 0 and c[1] != 0 and c[0][1] != 0 and c[2] > 3.5:
		myDrone.yaw_velocity = speed_rotation
		myDrone.for_back_velocity = speed_distance
		myDrone.up_down_velocity = speed_height
	else:
		myDrone.left_right_velocity = 0
		myDrone.for_back_velocity = 0
		myDrone.up_down_velocity = 0
		myDrone.yaw_velocity = 0
		error_rotation = 0
		error_distance = 0
		error_height = 0

	# SEND VELOCITY VALUES TO TELLO
	if myDrone.send_rc_control:
		myDrone.send_rc_control(myDrone.left_right_velocity,myDrone.for_back_velocity,
		myDrone.up_down_velocity, myDrone.yaw_velocity)

	return [error_rotation, error_distance, error_height]

def searchFace(myDrone, direction='up'):
	height = myDrone.get_height()
	if height <= 60:
		direction = 'up'
	elif height >= 160:
		direction = 'down'
	
	myDrone.up_down_velocity = 50 if direction=='up' else -50
	myDrone.yaw_velocity = 30
	myDrone.send_rc_control(0,0, myDrone.up_down_velocity, myDrone.yaw_velocity)

	return direction

def reactGest(myDrone, mode, gesture=None, pGest=None, gestCounter=0, myDroneIsTakeOff=True):
	if not gesture:
		return mode, None, 0, myDroneIsTakeOff
	if pGest == gesture:
		if gestCounter >= 5:
            

            # 1) WAIT FOR A COMMAND
			if gesture == "stop" and myDroneIsTakeOff:
				mode = "wait"

            # 2) LAND
			elif gesture=="peace" and myDroneIsTakeOff:
				myDrone.land()
				myDroneIsTakeOff = False

			# 3) TAKE OFF
			elif (gesture=="fist" or gesture=='thumbs down') and not myDroneIsTakeOff:
				myDrone.takeoff()
				myDroneIsTakeOff = True

			# 4) SHOW MY LOCATION
			elif (gesture == "thumbs up" or gesture=="call me") and myDroneIsTakeOff:
				myDrone.flip_back()
			
			# 5) SEARCH OTHER VICTIMS 
			elif gesture == "live long" and myDroneIsTakeOff:
				mode = "tracking"

			# 6) CAPTURE VIDEO AND SEND IT TO RESCUING TEAM
			elif gesture == "okay":
				mode = "video"
				
			gestCounter = 0
		else:
			gestCounter += 1

	else:
		gestCounter = 0

	return mode, gesture, gestCounter, myDroneIsTakeOff