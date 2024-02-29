#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Motorn för klon
gripper_motor = Motor(Port.A)

# Motor för armen
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Motor för basen
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Hastighetskrav
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Tar fram startpunkten av basen i förhållande till switch
base_switch = TouchSensor(Port.S1)

# Färg sensorn i armen
elbow_sensor = ColorSensor(Port.S3)

def calibration():
    # Kalibrera basens startposition
    base_motor.run(-60)
    while not base_switch.pressed():
        wait(10)
    base_motor.reset_angle(0)
    base_motor.hold()

    # Kalibrera klons startposition
    gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    gripper_motor.reset_angle(0)
    gripper_motor.run_target(200, -90)

    # Kalibrera armens startposition
    elbow_motor.run_time(-30, 1000)
    elbow_motor.run(15)
    while elbow_sensor.reflection() > 0:
        wait(10)
    elbow_motor.run_time(15, 250)
    elbow_motor.reset_angle(0)
    elbow_motor.hold()


    # Kalibreringen är klar efter 3 pip
    for i in range(3):
        ev3.speaker.beep()
        wait(100)

def robot_pick(pickup):
    base_motor.run_target(60, pickup)

    elbow_motor.run_target(60, -40)

    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)

    elbow_motor.run_target(30, 0)

def robot_release(position):
    base_motor.run_target(60, position)
    
    elbow_motor.run_target(30, -40)
    
    gripper_motor.run_target(200, -90)
    
    elbow_motor.run_target(60, 0)

def drop_location(color):
    # Pickup zone
    if 'RED' in color:
        robot_release(red)
    


    # Red zone
    # Green zone
    # Blue zone
    # Yellow zone

def setup_pickup():
    while True:
        base_motor.stop()
        if ev3.buttons.pressed(): 
            pickup = base_motor.angle()
            return pickup

def setup_dropoff():
    while True:
        base_motor.stop()
        if ev3.buttons.pressed(): 
            dropoff = base_motor.angle()
            return dropoff
    


            

def identify_color():
    current_color = elbow_sensor.color()
    ev3.speaker.say(current_color)
    print(current_color)
    drop_location(current_color)




if __name__ == "__main__":
    calibration()
    pickup = setup_pickup()
    wait(500)
    dropoff = setup_dropoff()
    robot_pick(pickup)
    robot_release(dropoff)


