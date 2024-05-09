#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait, StopWatch, DataLog
from time_script import get_current_time
ev3 = EV3Brick()

# General global ev3 variables
gripper_motor = Motor(Port.A)

elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

base_switch = TouchSensor(Port.S1)

elbow_sensor = ColorSensor(Port.S2)

# Change phases
change_phase = None


# Our own function because zfill dose not work with pybricks
def custom_zfill(string, width):
    if len(string) >= width:
        return string
    else:
        num_zeros = width - len(string)
        return '0' * num_zeros + string


def color_phase_menu(colors):
    ev3.screen.clear()
    ev3.screen.draw_text(10, 10, "^: drop off 1")
    ev3.screen.draw_text(10, 50, "v: drop off 2")
    ev3.screen.draw_text(50, 90, colors)


def zone_phase_menu():
    ev3.screen.clear()
    ev3.screen.draw_text(10, 10, "^: drop off 1")
    ev3.screen.draw_text(10, 30, "^ x 2: drop off 2")
    ev3.screen.draw_text(10, 50, "O: pickup")
    ev3.screen.draw_text(10, 70, "v: when done")


def main_menu(color):
    ev3.screen.clear()
    ev3.screen.draw_text(10, 10, "^: change zones")
    ev3.screen.draw_text(10, 30, "v: change colors")
    ev3.screen.draw_text(10, 50, "<: change times")
    ev3.screen.draw_text(10, 70, "O: pause")
    ev3.screen.draw_text(50, 90, color)


def time_menu(current_time, time_type, time_stamp_index):
    if time_stamp_index == 0:
        witch_time = "Starting Time"
    else:
        witch_time = "Ending Time"
    ev3.screen.clear()
    ev3.screen.draw_text(30, 10, "Change " + time_type)
    ev3.screen.draw_text(30, 30, witch_time)
    ev3.screen.draw_text(40, 65, current_time)


def calibration():
    base_motor.run(-60)
    while not base_switch.pressed():
        wait(10)
    base_motor.reset_angle(0)
    base_motor.hold()

    gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    gripper_motor.reset_angle(0)
    gripper_motor.run_target(200, -90)


    elbow_motor.run_time(-30, 1500)
    elbow_motor.run(15)
    while elbow_sensor.reflection() > 0:
        wait(530)
    elbow_motor.run_time(15, 250)
    elbow_motor.reset_angle(0)
    elbow_motor.hold()


    for i in range(3):
        ev3.speaker.beep()
        wait(100)


def left_or_right(position):
    if position > base_motor.angle():
        return 1
    else:
        return -1


def robot_move(part, speed, position):
    global change_phase
    if "C" in str(part):
        speed = (speed * left_or_right(position))
        part.run(speed)
    else:
        part.run(speed)
    robot_hold = False


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
            elif "UP" in btn:
                change_phase = "ZONE"
            elif "DOWN" in btn:
                change_phase = "COLOR"
            elif "LEFT" in btn:
                change_phase = "TIME"
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
    zone_phase_menu()
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
                if dropoff != None and dropoff_2 != None and pickup != None:
                    setup = False
                else:
                    ev3.speaker.say("You need to register 2 droppoff zones and one pickup zone")
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
        return None
    else:
        return current_color


def setup_colors():
    colors = ["GREEN", "RED", "YELLOW", "BLUE"]
    c_1 = []
    c_2 = []
    for color in colors:
        color_phase_menu(color)
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
    return [c_1, c_2]


def setup_time():
    start_time = get_current_time().split(":")
    end_time = get_current_time().split(":")
    times = [start_time, end_time]
    final_times = []
    time_types = ["Hour", "Minute", "Seconds"]
    time_stamp_index = 0
    for time_stamp in times:
        index = 0
        for time_type in time_types:
            time_menu(":".join(time_stamp), time_type, time_stamp_index)
            jonnyBravo = True
            wait(500)
            while jonnyBravo:
                if ev3.buttons.pressed() != []:
                    btn = str(ev3.buttons.pressed()[0])
                    if "UP" in btn:
                        time_stamp[index] = custom_zfill(str(int(time_stamp[index]) + 1), 2)
                        wait(500)
                        time_menu(":".join(time_stamp), time_type, time_stamp_index)
                    elif "DOWN" in btn:
                        time_stamp[index] = custom_zfill(str(int(time_stamp[index]) - 1), 2)
                        wait(500)
                        time_menu(":".join(time_stamp), time_type, time_stamp_index)
                    elif "CENTER" in btn:
                        jonnyBravo = False
                        wait(1000)

            index += 1
        time_stamp_index += 1
        final_times.append(":".join(time_stamp))
    return final_times


def sorted_release(color_list, current_color, dropoff, dropoff_2):
    if str(current_color) in color_list[0]:
        print("Releasing at dropoff 1")
        robot_release(dropoff)
    elif str(current_color) in color_list[1]:
        print("Releasing at dropoff 2")
        robot_release(dropoff_2)


def main():
    global change_phase
    current_color = None
    calibration()
    pickup, dropoff, dropoff_2 = setup_locations()
    color_list = setup_colors()
    starting_time, ending_time = setup_time()
    main_menu(current_color)
    wait(500)
    while True:
        if starting_time < get_current_time() < ending_time:
            robot_pick(pickup)
            current_color = identify_color()
            main_menu(current_color)
            wait(500)
            if current_color is not None:
                sorted_release(color_list, current_color, dropoff, dropoff_2)
        else:
            if ev3.buttons.pressed() != []:
                btn = str(ev3.buttons.pressed()[0])
                if "UP" in btn:
                    change_phase = "ZONE"
                elif "DOWN" in btn:
                    change_phase = "COLOR"
                elif "LEFT" in btn:
                    change_phase = "TIME"
        if change_phase == "ZONE":
            ev3.speaker.beep()
            wait(2000)
            pickup, dropoff, dropoff_2 = setup_locations()
            change_phase = None
            wait(500)
        elif change_phase == "COLOR":
            ev3.speaker.beep()
            wait(2000)
            color_list = setup_colors()
            change_phase = None
            wait(500)
        elif change_phase == "TIME":
            ev3.speaker.beep()
            wait(2000)
            starting_time, ending_time = setup_time()
            change_phase = None
            wait(500)


if __name__ == "__main__":
    main()
