import webiopi
import json
import configparser as ConfigParser
import RPi.GPIO as GPIO
import time
import os
from Robot import Robot


class InitioRobot(Robot):

    def __init__(self):
        self.__setProperties()
        self.__configurePins()

        # Enable debug output
        webiopi.setDebug()

    def __setProperties(self):
        # Pins 24, 26 Right Motor
        # Pins 19, 21 Left Motor
        self._r1 = 24
        self._r2 = 26
        self._l1 = 19
        self._l2 = 21

        # Define obstacle sensors and line sensors
        self._ir_left = 7
        self._ir_right = 11
        self._line_right = 13
        self._line_left = 12

        # Invert sensors if using IBoost64
        self._invert_ir_sensors = False

        # Define Sonar Pin (same pin for both Ping and Echo)
        # Note that this can be either 8 or 23 on PiRoCon
        self._sonar = 8

        # Check for overrides to the properties
        Config = ConfigParser.ConfigParser()
        Config.read('InitioRobot.ini')
        for property in Config.options('Properties'):
            prop = '_' + property
            val = Config.get('Properties', property)
            webiopi.debug('Found property ' + property + ' with value ' + val)
            if hasattr(self, prop):
                if val.isdigit():
                    setattr(self, prop, int(val))
                elif val == 'True':
                    setattr(self, prop, True)
                elif val == 'False':
                    setattr(self, prop, False)
                else:
                    setattr(self, prop, val)

    def __configurePins(self):
        # use physical pin numbering
        GPIO.setmode(GPIO.BOARD)

        # set up digital line detectors as inputs
        GPIO.setup(self._line_right, GPIO.IN)  # Right line sensor
        GPIO.setup(self._line_left, GPIO.IN)  # Left line sensor

        # Set up IR obstacle sensors as inputs
        GPIO.setup(self._ir_left, GPIO.IN)  # Left obstacle sensor
        GPIO.setup(self._ir_right, GPIO.IN)  # Right obstacle sensor

        # Set the wheel speed
        self.setFullSpeed(100)
        self.setTurnSpeed(10)

        # use pwm on inputs so motors don't go too fast
        # NOTE that using capitals in the property name prevents the properties
        #      from being overridden as ConfigParser is case insensitive and
        #      converts everything to lower case
        GPIO.setup(self._l1, GPIO.OUT)
        self._L1_pwm = GPIO.PWM(self._l1, 20)
        self._L1_pwm.start(0)

        GPIO.setup(self._l2, GPIO.OUT)
        self._L2_pwm = GPIO.PWM(self._l2, 20)
        self._L2_pwm.start(0)

        GPIO.setup(self._r1, GPIO.OUT)
        self._R1_pwm = GPIO.PWM(self._r1, 20)
        self._R1_pwm.start(0)

        GPIO.setup(self._r2, GPIO.OUT)
        self._R2_pwm = GPIO.PWM(self._r2, 20)
        self._R2_pwm.start(0)

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
        self._L1_pwm.ChangeDutyCycle(self._full_speed)
        self._L2_pwm.ChangeDutyCycle(0)
        self._R1_pwm.ChangeDutyCycle(self._full_speed)
        self._R2_pwm.ChangeDutyCycle(0)
        self._L1_pwm.ChangeFrequency(self._full_speed + 5)
        self._R1_pwm.ChangeFrequency(self._full_speed + 5)

    def stop(self):
        self._L1_pwm.ChangeDutyCycle(0)
        self._L2_pwm.ChangeDutyCycle(0)
        self._R1_pwm.ChangeDutyCycle(0)
        self._R2_pwm.ChangeDutyCycle(0)

    def reverse(self):
        self._L1_pwm.ChangeDutyCycle(0)
        self._L2_pwm.ChangeDutyCycle(self._full_speed)
        self._R1_pwm.ChangeDutyCycle(0)
        self._R2_pwm.ChangeDutyCycle(self._full_speed)
        self._L2_pwm.ChangeFrequency(self._full_speed + 5)
        self._R2_pwm.ChangeFrequency(self._full_speed + 5)

    def spinLeft(self):
        self._L1_pwm.ChangeDutyCycle(0)
        self._L2_pwm.ChangeDutyCycle(self._full_speed)
        self._R1_pwm.ChangeDutyCycle(self._full_speed)
        self._R2_pwm.ChangeDutyCycle(0)
        self._L2_pwm.ChangeFrequency(self._full_speed + 5)
        self._R1_pwm.ChangeFrequency(self._full_speed + 5)

    def spinRight(self):
        self._L1_pwm.ChangeDutyCycle(self._full_speed)
        self._L2_pwm.ChangeDutyCycle(0)
        self._R1_pwm.ChangeDutyCycle(0)
        self._R2_pwm.ChangeDutyCycle(self._full_speed)
        self._L1_pwm.ChangeFrequency(self._full_speed + 5)
        self._R2_pwm.ChangeFrequency(self._full_speed + 5)

    def forwardLeft(self):
        self._L1_pwm.ChangeDutyCycle(self._turn_speed)
        self._L2_pwm.ChangeDutyCycle(0)
        self._R1_pwm.ChangeDutyCycle(self._full_speed)
        self._R2_pwm.ChangeDutyCycle(0)
        self._L1_pwm.ChangeFrequency(self._turn_speed + 5)
        self._R1_pwm.ChangeFrequency(self._full_speed + 5)

    def forwardRight(self):
        self._L1_pwm.ChangeDutyCycle(self._full_speed)
        self._L2_pwm.ChangeDutyCycle(0)
        self._R1_pwm.ChangeDutyCycle(self._turn_speed)
        self._R2_pwm.ChangeDutyCycle(0)
        self._L1_pwm.ChangeFrequency(self._full_speed + 5)
        self._R1_pwm.ChangeFrequency(self._turn_speed + 5)

    def reverseLeft(self):
        self._L1_pwm.ChangeDutyCycle(0)
        self._L2_pwm.ChangeDutyCycle(self._turn_speed)
        self._R1_pwm.ChangeDutyCycle(0)
        self._R2_pwm.ChangeDutyCycle(self._full_speed)
        self._L2_pwm.ChangeFrequency(self._turn_speed + 5)
        self._R2_pwm.ChangeFrequency(self._full_speed + 5)

    def reverseRight(self):
        self._L1_pwm.ChangeDutyCycle(0)
        self._L2_pwm.ChangeDutyCycle(self._full_speed)
        self._R1_pwm.ChangeDutyCycle(0)
        self._R2_pwm.ChangeDutyCycle(self._turn_speed)
        self._L2_pwm.ChangeFrequency(self._full_speed + 5)
        self._R2_pwm.ChangeFrequency(self._turn_speed + 5)

    def irLeft(self):
        if (GPIO.input(self._ir_left) == 0 and not self._invert_ir_sensors) \
            or (GPIO.input(self._ir_left) != 0 and self._invert_ir_sensors):
            return True
        else:
            return False

    def irRight(self):
        if (GPIO.input(self._ir_right) == 0 and not self._invert_ir_sensors) \
            or (GPIO.input(self._ir_right) != 0 and self._invert_ir_sensors):
            return True
        else:
            return False

    def irAll(self):
        return self.irLeftStatus() or self.irRightStatus()

    def irLeftLine(self):
        if (GPIO.input(self._line_left) == 0 and not self._invert_ir_sensors) \
            or (GPIO.input(self._line_left) != 0 and self._invert_ir_sensors):
            return True
        else:
            return False

    def irRightLine(self):
        if (GPIO.input(self._line_right) == 0 and not self._invert_ir_sensors) \
            or (GPIO.input(self._line_right) != 0 and self._invert_ir_sensors):
            return True
        else:
            return False

    def getDistance(self):
        GPIO.setup(self._sonar, GPIO.OUT)
        # Send 10us pulse to trigger
        GPIO.output(self._sonar, True)
        time.sleep(0.00001)
        GPIO.output(self._sonar, False)
        start = time.time()
        count = time.time()
        GPIO.setup(self._sonar, GPIO.IN)
        while GPIO.input(self._sonar) == 0 and time.time() - count < 0.1:
            start = time.time()
            count = time.time()
            stop = count

        while GPIO.input(self._sonar) == 1 and time.time() - count < 0.1:
            stop = time.time()
            # Calculate pulse length
            elapsed = stop-start
            # Distance pulse travelled in that time is time
            # multiplied by the speed of sound (cm/s)
            distance = elapsed * 34000
            # That was the distance there and back so halve the value
            distance = distance / 2
            return distance

    def setFullSpeed(self, full_speed):
        if full_speed < 0:
            full_speed = 0
        elif full_speed > 100:
            full_speed = 100
        self._full_speed = full_speed

    def setTurnSpeed(self, turn_speed):
        if turn_speed < 0:
            turn_speed = 0
        elif turn_speed > 100:
            turn_speed = 100
        self._turn_speed = turn_speed

    def __setServo(self, Servo, Degrees):
        if not self._servos_active:
            self.__startServos()
            self.__pinServod (Servo, Degrees) # for now, simply pass on the input values

    def __stopServos(self):
        self.__stopServod()

    def __startServos(self):
        self.__startServod()

    def __startServod(self):
        SCRIPTPATH = os.path.split(os.path.realpath(__file__))[0]
        os.system(SCRIPTPATH +'/servod --idle-timeout=20000 --p1pins="18,22"')
        self._servos_active = True

    def __pinServod(self, pin, degrees):
        os.system("echo " + str(pin) + "=" + str(50+ ((90 - degrees) * 200 / 180)) + " > /dev/servoblaster")

    def __stopServod(self):
        os.system("sudo pkill -f servod")
        self._servos_active = False



