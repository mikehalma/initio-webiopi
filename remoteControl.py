import webiopi
from InitioRobot import InitioRobot
# from Robot import Robot

# Each macro provides a web service supported by webiopi that can be
# acccessed from the web application.
#
# Runs in the webiopi web server on its standard setup/loop/destroy loop


# Define pins for Pan/Tilt
pan = 0
tilt = 1
tVal = 0  # 0 degrees is centre
pVal = 0  # 0 degrees is centre
robot = None

# Configure the robot
def setup():
    global robot
    robot = InitioRobot()
#    robot = Robot()

# Kill all services
def destroy():
    global robot
    robot.destroy()

# We have nothing to do in the main loop as all services are made available
# as macros
def loop():
    global robot
    pass

# Placeholder for a macro which can adjust some servos
def doServos():
    global robot
#    initio.setServo(pan, pVal)
#    initio.setServo(tilt, tVal)

# Get the status of all IR sensors
@webiopi.macro
def irStatus():
    global robot
    return robot.irStatus()

# Move the robot forward until further notice
@webiopi.macro
def forward():
    global robot
    robot.forward()

# Stop the robot
@webiopi.macro
def stop():
    global robot
    robot.stop()

# Move the robot backwards until further notice
@webiopi.macro
def reverse():
    global robot
    robot.reverse()

# Spin the robot anti-clockwise until further notice
@webiopi.macro
def spinLeft():
    global robot
    robot.spinLeft()

# Spin the robot clockwise until further notice
@webiopi.macro
def spinRight():
    global robot
    robot.spinRight()

# Move the robot forward-left until further notice
@webiopi.macro
def forwardLeft():
    global robot
    robot.forwardLeft()

# Move the robot forward-right until further notice
@webiopi.macro
def forwardRight():
    global robot
    robot.forwardRight()

# Move the robot backwards-left until further notice
@webiopi.macro
def reverseLeft():
    global robot
    robot.reverseLeft()

# Move the robot backwards-right until further notice
@webiopi.macro
def reverseRight():
    global robot
    robot.reverseRight()
