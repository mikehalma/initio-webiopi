import initio
import webiopi
from InitioRobot import InitioRobot
# from Robot import Robot

# Define pins for Pan/Tilt
pan = 0
tilt = 1
tVal = 0  # 0 degrees is centre
pVal = 0  # 0 degrees is centre
robot = None


def setup():
    global robot
    robot = InitioRobot()
#    robot = Robot()


def destroy():
    global robot
    robot.destroy()


def loop():
    global robot
    pass


def doServos():
    global robot
    initio.setServo(pan, pVal)
    initio.setServo(tilt, tVal)


@webiopi.macro
def sonarUp():
    global pVal
    pVal += 10
    doServos()


@webiopi.macro
def irStatus():
    global robot
    return robot.irStatus()


@webiopi.macro
def forward():
    global robot
    robot.forward()


@webiopi.macro
def stop():
    global robot
    robot.stop()


@webiopi.macro
def reverse():
    global robot
    robot.reverse()


@webiopi.macro
def spinLeft():
    global robot
    robot.spinLeft()


@webiopi.macro
def spinRight():
    global robot
    robot.spinRight()


@webiopi.macro
def forwardLeft():
    global robot
    robot.forwardLeft()


@webiopi.macro
def forwardRight():
    global robot
    robot.forwardRight()


@webiopi.macro
def reverseLeft():
    global robot
    robot.reverseLeft()


@webiopi.macro
def reverseRight():
    global robot
    robot.reverseRight()
