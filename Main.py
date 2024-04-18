#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait, StopWatch, DataLog
# import time
# import datetime
ev3 = EV3Brick()

# Motorn för klon
gripper_motor = Motor(Port.A)

# Motor för armen
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Motor för basen
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Hastighetskrav
elbow_motor.control.limits(speed=60, acceleration=120)  # wtf är detta??? gör om förfan //Johan
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
    elbow_motor.run_time(-30, 1500)
    elbow_motor.run(15)
    while elbow_sensor.reflection() > 0:
        wait(530)
    elbow_motor.run_time(15, 250)
    elbow_motor.reset_angle(0)
    elbow_motor.hold()

    # Kalibreringen är klar efter 3 pip
    for i in range(3):
        ev3.speaker.beep()
        wait(100)


def left_or_right(position):
    if position > base_motor.angle():
        return 1
    else:
        return -1


def robot_move(part, speed, position):
    if "C" in str(part):
        part.run(speed * left_or_right(position))
    else:
        part.run(speed)
    robot_hold = False

    print(part)

    while not part.angle() == position:
        if ev3.buttons.pressed() != []:
            btn = str(ev3.buttons.pressed()[0])
            if "CENTER" in btn and robot_hold is False:
                part.hold()
                robot_hold = True
                wait(200)
            elif "CENTER" in btn:
                wait(200)
                part.run(speed)
                robot_hold = False
        wait(10)
    part.hold()


def robot_pick(position):
    gripper_motor.run_target(200, -90)

    robot_move(base_motor, 60, position)

    robot_move(elbow_motor, -60, -40)

    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)

    robot_move(elbow_motor, 30, 0)


def robot_release(position):
    robot_move(base_motor, 60, position)

    robot_move(elbow_motor, -30, -40)

    gripper_motor.run_target(200, -90)

    robot_move(elbow_motor, 60, 0)


def setup_locations():
    setup = True
    pickup = None
    dropoff = None
    dropoff_2 = None
    zones = 0

    base_motor.run(-60)
    while not base_switch.pressed():
        wait(10)

    while setup:
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


def identify_color():
    current_color = str(elbow_sensor.color())[6:]
    print(current_color)
    if current_color is None or current_color == 'BLACK':
        ev3.speaker.say("No color detected")
        return None
    else:
        return current_color


def setup_colors():
    colors = ["GREEN", "RED", "YELLOW", "BLUE"]
    c_1 = []
    c_2 = []
    for color in colors:
        ev3.screen.draw_text(10, 50, "Arrow up for DZone 1, Arrow down for DZone 2")
        ev3.screen.draw_text(40, 90, color)
        wait(500)
        while True:
            if ev3.buttons.pressed() != []:
                btn = str(ev3.buttons.pressed()[0])
                if "UP" in btn:
                    c_1.append(color)
                    break
                elif "DOWN" in btn:
                    c_2.append(color)
                    break
        ev3.screen.clear()
    return [c_1, c_2]


def sorted_release(color_list, current_color, dropoff, dropoff_2):
    if str(current_color) in color_list[0]:
        print("Releasing at dropoff 1")
        robot_release(dropoff)
    elif str(current_color) in color_list[1]:
        print("Releasing at dropoff 2")
        robot_release(dropoff_2)


def main():
    calibration()
    pickup, dropoff, dropoff_2 = setup_locations()
    color_list = setup_colors()
    # current_time = datetime.datetime.now().time()
    # start_time = datetime.time(14, 0)
    # end_time = datetime.time(14, 18)
    # while start_time <= current_time <= end_time:
    while True:
        robot_pick(pickup)
        current_color = identify_color()
        wait(500)
        if current_color is not None:
            sorted_release(color_list, current_color, dropoff, dropoff_2)
        if ev3.buttons.pressed() != []:
            btn = str(ev3.buttons.pressed()[0])
            if "UP" in btn:
                ev3.speaker.beep()
                wait(2000)
                pickup, dropoff, dropoff_2 = setup_locations()
            elif "DOWN" in btn:
                ev3.speaker.beep()
                wait(2000)
                color_list = setup_colors()
        # current_time = datetime.datetime.now().time()


if __name__ == "__main__":
    main()
