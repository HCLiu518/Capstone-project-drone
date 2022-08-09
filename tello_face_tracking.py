from util.utility import *
from util.utility_gesture import  *
from util.video_capture import *
import cv2
from threading import Thread


myDrone = intializeTello()
w, h = 360, 240
c = [[0,0],0,0]
pid = [0.5,0.5,0.5,0.5]
pError = [0,0,0]
pdirection = 'up'
pGest = None
findCounter = 0
gestCounter = 0
faceArea = w*h//16
myDroneIsTakeOff = True
mode = "tracking"
recorder = None

myDrone.takeoff()
print("My Battery: " + str(myDrone.get_battery()))

while True:

	## STEP 1
	img = telloGetFrame(myDrone, w, h)
	## STEP 2
	gesture = recogGest(img,w,h)
	if mode == "tracking":
		img, c = findFace(img)
	## STEP 3
	print(gesture)
	mode,pGest,gestCounter,myDroneIsTakeOff= reactGest(myDrone, mode, gesture, pGest, gestCounter, myDroneIsTakeOff)
	## STEP 4
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

	# DISPLAY IMAGE
	#cv2.imshow("MyResult", img.outline)
	cv2.imshow("MyResult", img)
	# WAIT FOR THE 'Q' BUTTON TO STOP
	if cv2.waitKey(1) and 0xFF == ord('q'):
		# replace the 'and' with '&amp;'  
		recorder.join()
		myDrone.land()
		break
	