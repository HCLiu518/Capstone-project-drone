from utility_yolo import *
import cv2

myDrone = intializeTello()
w, h = 360, 240
pid = [0.5,0.5,0]
pError = [0,0]
startCounter = 0

while True:

	if startCounter == 0:
		myDrone.takeoff()
		#myDrone.move('up',20)
		startCounter = 1

	## STEP 1
	img = telloGetFrame(myDrone, w, h)
	## STEP 2
	img, c = findFace(img)
	## STEP 3
	pError = trackFace(myDrone,c,w,pid,pError)
	# DISPLAY IMAGE
	cv2.imshow("MyResult", img)
	# WAIT FOR THE 'Q' BUTTON TO STOP
	if cv2.waitKey(1) and 0xFF == ord('q'):
		# replace the 'and' with '&amp;'  
		myDrone.land()
		break