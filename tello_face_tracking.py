from util.utility import *
from util.utility_gesture import  *
from util.video_capture import *
import cv2
from threading import Thread

## Initiate the drone
myDrone = intializeTello()

## Setup parameters
w, h = 360, 240 # width and height of capture images
c = [[0,0],0,0] # parameter of faces
pid = [0.5,0.5,0.5,0.5] # PID
pError = [0,0,0] # previous error of PID
pdirection = 'up' # previous direction of searching face
pGest = None # previous gesture of gesture recognition
findCounter = 0 # counter for starting to search faces
gestCounter = 0 # counter for responding to the gesture
faceArea = w*h//16
myDroneIsTakeOff = True
mode = "tracking" # three modes: tracking, wait, video
recorder = None

## Take off the drone
myDrone.takeoff()

while True:

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
			pError = trackFace(myDrone,c,w,h,faceArea,pid,pError)
			if c[0][0] == 0 and c[1] == 0 and c[0][1] == 0:
				findCounter += 1
			else:
				findCounter = 0

	elif mode == "wait":
		pError = [0,0,0]
		findCounter = 101
		c = [[0,0],0,0]
		_ = trackFace(myDrone,c,w,h,faceArea,pid,pError)

	elif mode == "video":
		pError = [0,0,0]
		findCounter = 101
		c = [[0,0],0,0]
		_ = trackFace(myDrone,c,w,h,faceArea,pid,pError)
		recorder = Thread(target=capture_video, args=(myDrone, img))
		recorder.start()
		mode = "wait"

	## Displat image
	cv2.imshow("MyResult", img)
	# WAIT FOR THE 'Q' BUTTON TO STOP
	if cv2.waitKey(1) and 0xFF == ord('q'):
		recorder.join()
		myDrone.land()
		break
	