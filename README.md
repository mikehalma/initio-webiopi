# initio-webiopi
This project provides a web interface to the [4tronix initio robot](http://4tronix.co.uk/blog/?p=169) using the [webiopi web server](https://code.google.com/p/webiopi/) for the raspberry pi.

The web app shows the status of the IR sensors and provides buttons for controlling the robot.  Work is in progress to add controls for the sonar and provide information from the wheel sensors.

The web app controller has been abstracted from the robot controller meaning that this web app can easily be used for different robots.

![ScreenShot](https://cloud.githubusercontent.com/assets/5145474/6135428/6624aca8-b160-11e4-8d46-3342bbabcc83.png)

# Get it working
* [Install webiopi](https://code.google.com/p/webiopi/wiki/INSTALL)
* Clone this repository onto the raspberry pi:
  * Git should already be installed if you are using the initio.  If not use the command "*sudo apt-get install git*" to install git.
  * To clone the repository, run the command "*git clone https://github.com/mikehalma/initio-webiopi.git*", which will create a directory called initio-webiopi
* Change the webiopi config file to point at the project
  * In /etc/webiopi/config, add a line to the [SCRIPTS] section - "*remoteControl = /home/pi/path/to/project/remoteControl.py*"
  * In /etc/webiopi/config, add a line to the [HTML] section - "*doc-root = /home/pi/path/to/project/html*"
  * Note that anything else found in the [SCRIPTS] or [HTML] sections should be commented out  
* Now follow the instructions on the [webiopi wiki](https://code.google.com/p/webiopi/wiki/INSTALL) to start the web server
* Locate the IP address of the raspberry pi on your network - run command "*ip addr show | grep inet | grep global*" and the IP address should be of the format 192.168.x.y
* Type the following address into a browser also on your network - e.g. http://192.168.x.y:8000

# Get it working with different pins
If you have changed any of the pins from those recommended in the initio build instructions, you can change the pin numbers in InitioRobot.ini to override the defaults.

# Get it working with inverted IR sensors
If you have a newer version of the robot you might have an extra chip to regulate the IR sensors (the iBoost64).  Unfortunately this also inverts the signals from the sensors.

In InitioRobot.ini, uncomment the line *invert_ir_sensors: True*.

# Get it working for a different robot
* Copy InitioRobot.py to make a new robot controller
* In remoteControl.py, change from the InitioRobot to the new robot controller you have created
* Note that you only need to implement the methods found in the base class Robot.py - the other stuff in InitioRobot.py is currently in progress (servos etc).
* If you do not implement a method from Robot.py then the robot will ignore that command from the web app
