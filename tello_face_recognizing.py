from util.utility import *
from util.utility_recognition import *
import cv2
import time

## Initiate the drone
myDrone = intializeTello()

## Setup parameters
w, h = 360, 240 # width and height of capture images
c = [[0,0],0,0] # parameter of faces
pid =  [[0.3,0.3,0],[0.5,0.5,0],[0.5,0.5,0]]# PID
pError = [0,0,0] # previous error of PID
faceArea = w*h//16
#counterCycles = 0
#counterDetection = 0

## Take off the drone
myDrone.takeoff()
myDrone.move_up(100)

while True:
	#counterCycles += 1
	start_time = time.perf_counter()
	## STEP 1: get a image from the drone
	img = telloGetFrame(myDrone, w, h)
	## STEP 2: Recogize people and send back whether it is person of interest or not.
	img, c = recognition(img, "Volunteer")
	## STEP 3: if it is person of interest, then the drone track the person.
	pError,_ = trackFace(myDrone,c,w,h,faceArea,pid,pError)
	#if c[1] != 0:
		#counterDetection += 1

	## display image
	cv2.imshow("MyResult", img)
	# WAIT FOR THE 'Q' BUTTON TO STOP
	if cv2.waitKey(1) and 0xFF == ord('q'):
		myDrone.land()
		break
	
	#print("Cycle counter: ", str(counterCycles))
	#print("Detection counter: ", str(counterDetection))
	#duration = start_time - time.perf_counter()
	#print(f"Duration of one cycle: {duration:0.4f}")