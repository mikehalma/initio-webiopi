import webiopi, json
import RPi.GPIO as GPIO, sys, threading, time, os
from Robot import Robot

class InitioRobot(Robot):

    def __init__(self):
        self.full_speed = 100
        self.turn_speed = 10

        self.__setPins()
        self.__configurePins()

        # Invert sensors if using IBoost64
        self.invert_ir_sensors = True

        # Enable debug output
        webiopi.setDebug()

    def __setPins(self):
        # Pins 24, 26 Right Motor
        # Pins 19, 21 Left Motor
        self.R1 = 24
        self.R2 = 26
        self.L1 = 19
        self.L2 = 21

        # Define obstacle sensors and line sensors
        self.irFL = 7
        self.irFR = 11
        self.lineRight = 13
        self.lineLeft = 12

        # Define Sonar Pin (same pin for both Ping and Echo)
        # Note that this can be either 8 or 23 on PiRoCon
        self.sonar = 8

        # Override default pins
        # todo - get overrides from property file

    def __configurePins(self):
        #use physical pin numbering
        GPIO.setmode(GPIO.BOARD)

        #set up digital line detectors as inputs
        GPIO.setup(self.lineRight, GPIO.IN)  # Right line sensor
        GPIO.setup(self.lineLeft, GPIO.IN)  # Left line sensor

        #Set up IR obstacle sensors as inputs
        GPIO.setup(self.irFL, GPIO.IN)  # Left obstacle sensor
        GPIO.setup(self.irFR, GPIO.IN)  # Right obstacle sensor

        #use pwm on inputs so motors don't go too fast
        GPIO.setup(self.L1, GPIO.OUT)
        self.L1_pwm = GPIO.PWM(self.L1, 20)
        self.L1_pwm.start(0)

        GPIO.setup(self.L2, GPIO.OUT)
        self.L2_pwm = GPIO.PWM(self.L2, 20)
        self.L2_pwm.start(0)

        GPIO.setup(self.R1, GPIO.OUT)
        self.R1_pwm = GPIO.PWM(self.R1, 20)
        self.R1_pwm.start(0)

        GPIO.setup(self.R2, GPIO.OUT)
        self.R2_pwm = GPIO.PWM(self.R2, 20)
        self.R2_pwm.start(0)

        self.__startServos()

    def destroy(self):
        self.stop()
        GPIO.cleanup()

    def irStatus(self):
        status = {}
        status["left"] = self.irLeft()
        status["leftLine"] = self.irLeftLine()
        status["right"] = self.irRight()
        status["rightLine"] = self.irRightLine()
        return json.dumps(status)

    def forward(self):
        self.L1_pwm.ChangeDutyCycle(self.full_speed)
        self.L2_pwm.ChangeDutyCycle(0)
        self.R1_pwm.ChangeDutyCycle(self.full_speed)
        self.R2_pwm.ChangeDutyCycle(0)
        self.L1_pwm.ChangeFrequency(self.full_speed + 5)
        self.R1_pwm.ChangeFrequency(self.full_speed + 5)

    def stop(self):
        self.L1_pwm.ChangeDutyCycle(0)
        self.L2_pwm.ChangeDutyCycle(0)
        self.R1_pwm.ChangeDutyCycle(0)
        self.R2_pwm.ChangeDutyCycle(0)

    def reverse(self):
        self.L1_pwm.ChangeDutyCycle(0)
        self.L2_pwm.ChangeDutyCycle(self.full_speed)
        self.R1_pwm.ChangeDutyCycle(0)
        self.R2_pwm.ChangeDutyCycle(self.full_speed)
        self.L2_pwm.ChangeFrequency(self.full_speed + 5)
        self.R2_pwm.ChangeFrequency(self.full_speed + 5)

    def spinLeft(self):
        self.L1_pwm.ChangeDutyCycle(0)
        self.L2_pwm.ChangeDutyCycle(self.full_speed)
        self.R1_pwm.ChangeDutyCycle(self.full_speed)
        self.R2_pwm.ChangeDutyCycle(0)
        self.L2_pwm.ChangeFrequency(self.full_speed + 5)
        self.R1_pwm.ChangeFrequency(self.full_speed + 5)

    def spinRight(self):
        self.L1_pwm.ChangeDutyCycle(self.full_speed)
        self.L2_pwm.ChangeDutyCycle(0)
        self.R1_pwm.ChangeDutyCycle(0)
        self.R2_pwm.ChangeDutyCycle(self.full_speed)
        self.L1_pwm.ChangeFrequency(self.full_speed + 5)
        self.R2_pwm.ChangeFrequency(self.full_speed + 5)

    def forwardLeft(self):
        self.L1_pwm.ChangeDutyCycle(self.turn_speed)
        self.L2_pwm.ChangeDutyCycle(0)
        self.R1_pwm.ChangeDutyCycle(self.full_speed)
        self.R2_pwm.ChangeDutyCycle(0)
        self.L1_pwm.ChangeFrequency(self.turn_speed + 5)
        self.R1_pwm.ChangeFrequency(self.full_speed + 5)

    def forwardRight(self):
        self.L1_pwm.ChangeDutyCycle(self.full_speed)
        self.L2_pwm.ChangeDutyCycle(0)
        self.R1_pwm.ChangeDutyCycle(self.turn_speed)
        self.R2_pwm.ChangeDutyCycle(0)
        self.L1_pwm.ChangeFrequency(self.full_speed + 5)
        self.R1_pwm.ChangeFrequency(self.turn_speed + 5)

    def reverseLeft(self):
        self.L1_pwm.ChangeDutyCycle(0)
        self.L2_pwm.ChangeDutyCycle(self.turn_speed)
        self.R1_pwm.ChangeDutyCycle(0)
        self.R2_pwm.ChangeDutyCycle(self.full_speed)
        self.L2_pwm.ChangeFrequency(self.turn_speed + 5)
        self.R2_pwm.ChangeFrequency(self.full_speed + 5)

    def reverseRight(self):
        self.L1_pwm.ChangeDutyCycle(0)
        self.L2_pwm.ChangeDutyCycle(self.full_speed)
        self.R1_pwm.ChangeDutyCycle(0)
        self.R2_pwm.ChangeDutyCycle(self.turn_speed)
        self.L2_pwm.ChangeFrequency(self.full_speed + 5)
        self.R2_pwm.ChangeFrequency(self.turn_speed + 5)


    def irLeft(self):
        if (GPIO.input(self.irFL) == 0 and not self.invert_ir_sensors) \
            or (GPIO.input(self.irFL) != 0 and self.invert_ir_sensors):
            return True
        else:
            return False

    def irRight(self):
        if (GPIO.input(self.irFR) == 0 and not self.invert_ir_sensors) \
            or (GPIO.input(self.irFR) != 0 and self.invert_ir_sensors):
            return True
        else:
            return False

    def irAll(self):
        return self.irLeftStatus() or self.irRightStatus()

    def irLeftLine(self):
        if (GPIO.input(self.lineLeft) == 0 and not self.invert_ir_sensors) \
            or (GPIO.input(self.lineLeft) != 0 and self.invert_ir_sensors):
            return True
        else:
            return False

    def irRightLine(self):
        if (GPIO.input(self.lineRight) == 0 and not self.invert_ir_sensors) \
            or (GPIO.input(self.lineRight) != 0 and self.invert_ir_sensors):
            return True
        else:
            return False

    def getDistance(self):
        GPIO.setup(self.sonar, GPIO.OUT)
        # Send 10us pulse to trigger
        GPIO.output(self.sonar, True)
        time.sleep(0.00001)
        GPIO.output(self.sonar, False)
        start = time.time()
        count=time.time()
        GPIO.setup(self.sonar, GPIO.IN)
        while GPIO.input(self.sonar) == 0 and time.time() - count < 0.1:
            start = time.time()
            count=time.time()
            stop=count

        while GPIO.input(self.sonar) == 1 and time.time() - count < 0.1:
            stop = time.time()
            # Calculate pulse length
            elapsed = stop-start
            # Distance pulse travelled in that time is time
            # multiplied by the speed of sound (cm/s)
            distance = elapsed * 34000
            # That was the distance there and back so halve the value
            distance = distance / 2
            return distance

    def __setServo(Servo, Degrees):
        if self.servos_active == False:
            self.__startServos()
            self.__pinServod (Servo, Degrees) # for now, simply pass on the input values

    def __stopServos(self):
        self.__stopServod()

    def __startServos(self):
        self.__startServod()

    def __startServod(self):
        SCRIPTPATH = os.path.split(os.path.realpath(__file__))[0]
        os.system(SCRIPTPATH +'/servod --idle-timeout=20000 --p1pins="18,22"')
        self.servos_active = True

    def __pinServod(pin, degrees):
        os.system("echo " + str(pin) + "=" + str(50+ ((90 - degrees) * 200 / 180)) + " > /dev/servoblaster")

    def __stopServod(self):
        os.system("sudo pkill -f servod")
        self.servos_active = False



