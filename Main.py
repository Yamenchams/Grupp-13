#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

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
elbow_sensor = ColorSensor(Port.S2)


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


def setup_locations():
    setup = True
    pickup = None
    dropoff = None
    dropoff_2 = None
    zones = 0
    while setup == True:
        base_motor.stop()
        if ev3.buttons.pressed() != []:
            btn = str(ev3.buttons.pressed()[0])
            if "CENTER" in btn:
                pickup = base_motor.angle()
            elif "UP" in btn and zones == 0:
                dropoff = base_motor.angle()
                zones += 1
                print("First zone registered")
                wait(500)
            elif "UP" in btn and zones == 1:
                dropoff_2 = base_motor.angle()
                print("Second zone registered")
                wait(500)
            elif "DOWN" in btn:
                setup = False
            elif "LEFT" in btn:
                base_motor.run(60)
                wait(400)
            elif "RIGHT" in btn:
                base_motor.run(-60)
                wait(400)
    return pickup, dropoff, dropoff_2


def identify_color(pickup):
    current_color = elbow_sensor.color()
    
    if current_color == None:
        robot_pick(pickup)
        identify_color()
        
    print(current_color)
    return current_color


def color_sorting():
    c_1 = "Color.GREEN"
    c_2 = "Color.RED"
    return [c_1, c_2]


def sorted_release(color_list, current_color, dropoff, dropoff_2):
    if current_color == str(color_list[0]):
        print("Releasing at Green")
        robot_release(dropoff)
    elif current_color == str(color_list[1]):
        print("Releasing at Red")
        robot_release(dropoff_2)


if __name__ == "__main__":
    calibration()
    pickup, dropoff, dropoff_2 = setup_locations()
    color_list = color_sorting()
    robot_pick(pickup)
    current_color = identify_color(pickup)
    sorted_release(color_list, current_color, dropoff, dropoff_2)
