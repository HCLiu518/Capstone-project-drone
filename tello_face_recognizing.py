from util.utility import *
from util.utility_recognition import *

import cv2



myDrone = intializeTello()
w, h = 360, 240
c = [[0,0],0,0]
pid = [0.5,0.5,0.5,0.5]
pError = [0,0,0]
faceArea = w*h//16


myDrone.takeoff()
print("My Battery: " + str(myDrone.get_battery()))

while True:

	## STEP 1
	img = telloGetFrame(myDrone, w, h)
	## STEP 2
	img, c = recognition(img, "Hung-Chih Liu")
	## STEP 3
	pError = trackFace(myDrone,c,w,h,faceArea,pid,pError)

	# DISPLAY IMAGE
	cv2.imshow("MyResult", img)
	# WAIT FOR THE 'Q' BUTTON TO STOP
	if cv2.waitKey(1) and 0xFF == ord('q'):
		# replace the 'and' with '&amp;'  
		myDrone.land()
		break
	