import time
import cv2
from threading import Thread
from util.utility import telloGetFrame

## Function for capturing video
def capture_video(myDrone, img, w=360, h=240):

	keepRecording = True

	## helper function for capturing video
	def video_recorder():

		video = cv2.VideoWriter('./outputs/recording.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (w,h))

		while keepRecording:
			video.write(telloGetFrame(myDrone))
			## 30 frames per second
			time.sleep(1 / 30)

		video.release()
	
	## open a thread
	recorder = Thread(target=video_recorder)
	recorder.start()

	## stop recording after 10 seconds
	time.sleep(10000)
	keepRecording = False

	recorder.join()
	return None