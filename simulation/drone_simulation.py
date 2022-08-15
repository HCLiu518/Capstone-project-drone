import setup_path
import airsim
import numpy as np
import os
import tempfile
import pprint
import cv2
import time

###CONNECT###

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)
client.takeoffAsync().join()

airsim.wait_key('Press any key to start recording')
client.startRecording()


###ROTATE###

vx = 0
vy = 0
z = -3
duration = 3
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 90)).join()
time.sleep(1)


###MOVE FORWARD###

vx = 2
vy = 0
z = -3
duration = 15
client.moveByVelocityZAsync(vx, vy, z, duration).join()
time.sleep(1)

###ROTATE###

vx = 0
vy = 0
z = -3
duration = 3
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 180)).join()
time.sleep(1)


###MOVE RIGHT###

vx = 0
vy = 2
z = -3
duration = 12
client.moveByVelocityZAsync(vx, vy, z, duration).join()
time.sleep(1)

###ROTATE###

vx = 0
vy = 0
z = -3
duration = 3
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 270)).join()
time.sleep(1)

###MOVE BACKWARD###

vx = -2
vy = 0
z = -3
duration = 15
client.moveByVelocityZAsync(vx, vy, z, duration).join()
time.sleep(1)

###ROTATE###

vx = 0
vy = 0
z = -3
duration = 3
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()
time.sleep(1)

###MOVE LEFT###

vx = 0
vy = -2
z = -3
duration = 12
client.moveByVelocityZAsync(vx, vy, z, duration).join()
time.sleep(1)

###STOP###

client.stopRecording()
airsim.wait_key('Press any key to stop the simulation')
client.armDisarm(False)
client.reset()
client.enableApiControl(False)
