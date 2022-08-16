import math

import cv2
from djitellopy import tello
from time import sleep

import numpy as np
import util.KeyPressModule as kp

## parameters for drawing
fSpeed = 117/10 # Forward speed in cm per second (15cm/s)
aSpeed = 360/10 # Angular speed in deg per second (50degrees/s)
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval

## the drone status
x, y = 500, 500
a = 0 #angle
yaw = 0 #yaw

## initialize the module and drone
kp.init()
me = tello.Tello()
me.connect()
me.streamoff()
me.streamon()
print(me.get_battery())

points = [(0,0), (0,0)]

## helper function for handling keyboard inputs
def getKeyInput(a=0):
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    global x, y, yaw
    d = 0 # distance

    # Roll Inputs
    if kp.getKey("LEFT"):
        lr = -speed
    #linear and angular distance change
        d = dInterval
        a = 180
    elif kp.getKey("RIGHT"):
        lr = speed
    # linear and angular distance change
        d = dInterval
        a = 0

    # Pitch Inputs
    if kp.getKey("UP"):
        fb = speed
    # linear and angular distance change
        d = dInterval
        if kp.getKey("LEFT"):
            a = (a + 270)/2
        elif kp.getKey("RIGHT"):
            a = 315
        else:
            a = 270
    elif kp.getKey("DOWN"):
        fb = -speed
    # linear and angular distance change
        d = dInterval
        if kp.getKey("LEFT") or kp.getKey("RIGHT"):
            a = (a + 90)/2
        else:
            a = 90


    # Throttle Inputs
    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    # Yaw Inputs
    if kp.getKey("a"):
        yv = -aspeed
        yaw -= aInterval # angular distance change
    elif kp.getKey("d"):
        yv = aspeed
        yaw += aInterval # angular distance change
    # Land Inputs
    if kp.getKey("q"): me.land()

    # Take-Off Inputs
    if kp.getKey("e"): me.takeoff()
    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]

## helper function for drawing the floorplan
def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED) #BGR direction
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED) #heading
    cv2.putText(img, f'({(points[-1][0] - 500) / 100}, {(points[-1][1] - 500) / 100} )m', (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    #create points

while True:

    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))

    drawPoints(img, points)

    cv2.imshow("Output:", img)
    cv2.waitKey(1)