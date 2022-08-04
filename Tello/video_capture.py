import time
import cv2
from threading import Thread
from utility import telloGetFrame

def capture_video(myDrone, img, w=360, h=240):

	keepRecording = True
	#myDrone.streamon()

	def video_recorder():

		video = cv2.VideoWriter('recording.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (w,h))

		while keepRecording:
			video.write(telloGetFrame(myDrone))
			time.sleep(1 / 30)

		video.release()

	recorder = Thread(target=video_recorder)
	recorder.start()
	time.sleep(10000)
	keepRecording = False
	recorder.join()
	return None