
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

ev3 = EV3Brick()

# Motorn för klon
gripper_motor = Motor(Port.A)

# Motor för armen
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Motor för basen
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Hastighetskrav
# elbow_motor.control.limits(speed=60, acceleration=120)
# base_motor.control.limits(speed=60, acceleration=120)

# Tar fram startpunkten av basen i förhållande till switch
base_switch = TouchSensor(Port.S1)

# Färg sensorn i armen
elbow_sensor = ColorSensor(Port.S3)

while True:
    print(elbow_sensor.reflection())

# # Kalibrera armens startposition
# elbow_motor.run_time(-30, 1000)
# elbow_motor.run(15)
# while elbow_sensor.reflection() < 32:
#     wait(10)
# elbow_motor.reset_angle(0)
# elbow_motor.hold()

# # Kalibrera basens startposition
# base_motor.run(-60)
# while not base_switch.pressed():
#     wait(10)
# base_motor.reset_angle(0)
# base_motor.hold()

# # Kalibrera klons startposition
# gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
# gripper_motor.reset_angle(0)
# gripper_motor.run_target(200, -90)

# # Kalibreringen är klar efter 3 pip
# for i in range(3):
#     ev3.speaker.beep()
#     wait(100)
