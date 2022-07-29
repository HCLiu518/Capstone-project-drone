from djitellopy import Tello
import time
tello = Tello()

tello.connect()
tello.takeoff()

#tello.move_left(100)
tello.rotate_clockwise(90)
#tello.move_forward(100)

tello.land()
time.sleep(10)
tello.connect()
tello.takeoff()

#tello.move_left(100)
tello.rotate_clockwise(90)
#tello.move_forward(100)

tello.land()