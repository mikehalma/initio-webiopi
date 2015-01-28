import sys, time
import initio
import webiopi

straight_speed = 100
straight_time = 0.2
spin_speed = 100
spin_time = 0.5

def setup():
    initio.init()

def loop():
    if initio.irAll():
        if not initio.irLeft():
            print 'Right ir acivated'
            initio.spinLeft(spin_speed)
            time.sleep(spin_time)
        elif not initio.irRight():
            print 'Left ir acivated'
            initio.spinRight(spin_speed)
            time.sleep(spin_time)
        else:
            print 'Both irs activated'
            initio.spinLeft(spin_speed)
            time.sleep(spin_time)
    else:
        print 'Moving forward'
        initio.forward(straight_speed)
        time.sleep(straight_time)

def destroy():
    initio.cleanup()
