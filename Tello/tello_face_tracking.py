from utility import *
from utility_gesture import  *
import cv2
from hand_detection import  *
import handy


myDrone = intializeTello()
w, h = 360, 240
pid = [0.5,0.5,0.5,0.5]
pError = [0,0,0]
pdirection = 'up'
pGest = None
findCounter = 0
gestCounter = 0
faceArea = w*h//16

myDrone.takeoff()
#hist = handy.capture_histogram(myDrone, 0, w, h)
print("My Battery: " + str(myDrone.get_battery()))

while True:

	## STEP 1
	img = telloGetFrame(myDrone, w, h)
	## STEP 2
	gesture = recogGest(img,w,h)
	img, c = findFace(img)
	#img = handDetection(img,hist)
	## STEP 3
	print(gesture)
	print(myDrone.get_height())
	pGest,gestCounter = reactGest(myDrone, gesture, pGest, gestCounter)
	## STEP 4
	if c[0][0] == 0 and c[1] == 0 and c[0][1] == 0 and findCounter > 100:
		pdirection = searchFace(myDrone, pdirection)
	else:
		pError = trackFace(myDrone,c,w,h,faceArea,pid,pError)
		#print(findCounter)
		if c[0][0] == 0 and c[1] == 0 and c[0][1] == 0:
			findCounter += 1
		else:
			findCounter = 0
	# DISPLAY IMAGE
	#cv2.imshow("MyResult", img.outline)
	cv2.imshow("MyResult", img)
	# WAIT FOR THE 'Q' BUTTON TO STOP
	if cv2.waitKey(1) and 0xFF == ord('q'):
		# replace the 'and' with '&amp;'  
		myDrone.land()
		break
	