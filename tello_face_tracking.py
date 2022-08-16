from util.utility import *
from util.utility_gesture import  *
from util.video_capture import *
import cv2
from threading import Thread
import time
import matplotlib as mpl
import matplotlib.pyplot as plt

## Initiate the drone
myDrone = intializeTello()

## Setup parameters
w, h = 360, 240 # width and height of capture images
c = [[0,0],0,0] # parameter of faces
pid = [[0.3,0.3,0],[0.5,0.5,0],[0.5,0.5,0]] # 3 PID controllers, one for rotation, one for for-back, one for up-down
pError = [0,0,0] # previous error of PID
pdirection = 'up' # previous direction of searching face
pGest = None # previous gesture of gesture recognition
findCounter = 0 # counter for starting to search faces
gestCounter = 0 # counter for responding to the gesture
faceArea = w*h//16
myDroneIsTakeOff = True
mode = "tracking" # three modes: tracking, wait, video
recorder = None

#timeList = []
#speedList = []
#speed = [0,0,0]

## Take off the drone
myDrone.takeoff()
#start_time = time.perf_counter()
myDrone.move_up(150)

while True:
	#duration = time.perf_counter() - start_time
	#timeList.append(duration)
	#speedList.append(speed[2])
	#speed = [0,0,0]
	## STEP 1: get a image from the drone
	img = telloGetFrame(myDrone, w, h)
	## STEP 2: recognize the gesture and faces if in the tracking mode
	gesture = recogGest(img,w,h)
	if mode == "tracking":
		img, c = findFace(img)
	## STEP 3: handle the response of gesture
	print(gesture)
	mode,pGest,gestCounter,myDroneIsTakeOff= reactGest(myDrone, mode, gesture, pGest, gestCounter, myDroneIsTakeOff)
	## STEP 4:
	### Tracking mode: track the biggest face and search for one if there is not any face after 100 counts.
	### Wait mode: stand still and only do recognizing gesture
	### Video mode: start to record video and swith back to wait mode immediately
	if mode == "tracking":
		if c[0][0] == 0 and c[1] == 0 and c[0][1] == 0 and findCounter > 100:
			pdirection = searchFace(myDrone, pdirection)
		else:
			pError, speed = trackFace(myDrone,c,w,h,faceArea,pid,pError)
			if c[0][0] == 0 and c[1] == 0 and c[0][1] == 0:
				findCounter += 1
			else:
				findCounter = 0

	elif mode == "wait":
		pError = [0,0,0]
		findCounter = 101
		c = [[0,0],0,0]
		_, __ = trackFace(myDrone,c,w,h,faceArea,pid,pError)

	elif mode == "video":
		pError = [0,0,0]
		findCounter = 101
		c = [[0,0],0,0]
		_, __ = trackFace(myDrone,c,w,h,faceArea,pid,pError)
		recorder = Thread(target=capture_video, args=(myDrone, img))
		recorder.start()
		mode = "wait"

	## Displat image
	cv2.imshow("MyResult", img)
	# WAIT FOR THE 'Q' BUTTON TO STOP
	if cv2.waitKey(1) == ord('q'):
		#recorder.join()
		myDrone.land()
		break
	
	

	#print(f"Duration of one cycle: {duration:0.4f}")
#plt.plot(timeList,speedList,label='PID = [0.65,0.65,0]',color="blue")
#plt.xlabel('Time')
#plt.ylabel('Speed of distance')
#plt.legend()
#plt.show()

#plt.plot(timeList,speedList,label='PID = [0.65,0.65,0]',color="red")
#plt.xlabel('Time')
#plt.ylabel('Speed of rotation')
#plt.legend()
#plt.show()

#plt.plot(timeList,speedList,label='PID = [1.0,1.0,0]',color="black")
#plt.xlabel('Time')
#plt.ylabel('Speed of height')
#plt.legend()
#plt.show()