from util.utility import *
from util.utility_recognition import *
import cv2

## Initiate the drone
myDrone = intializeTello()

## Setup parameters
w, h = 360, 240 # width and height of capture images
c = [[0,0],0,0] # parameter of faces
pid = [0.5,0.5,0.5,0.5] # PID
pError = [0,0,0] # previous error of PID
faceArea = w*h//16

## Take off the drone
myDrone.takeoff()

while True:

	## STEP 1: get a image from the drone
	img = telloGetFrame(myDrone, w, h)
	## STEP 2: Recogize people and send back whether it is person of interest or not.
	img, c = recognition(img, "Hung-Chih Liu")
	## STEP 3: if it is person of interest, then the drone track the person.
	pError = trackFace(myDrone,c,w,h,faceArea,pid,pError)

	## display image
	cv2.imshow("MyResult", img)
	# WAIT FOR THE 'Q' BUTTON TO STOP
	if cv2.waitKey(1) and 0xFF == ord('q'):
		myDrone.land()
		break
	