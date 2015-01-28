import initio
import webiopi

# Define pins for Pan/Tilt
pan = 0
tilt = 1
tVal = 0 # 0 degrees is centre
pVal = 0 # 0 degrees is centre

def setup():
    initio.init()

def destroy():
    initio.cleanup()

def loop():
    pass

def doServos():
    initio.setServo(pan, pVal)
    initio.setServo(tilt, tVal)


@webiopi.macro
def sonarUp():
    global pVal
    pVal += 10
    doServos()
   
@webiopi.macro
def leftIrStatus():
    if initio.irLeft():
        return '{"status":true}'
    else:
        return '{"status":false}'

@webiopi.macro
def forward():
    initio.forward(100)

@webiopi.macro
def stop():
    initio.stop()

@webiopi.macro
def reverse():
    initio.reverse(100)
    
@webiopi.macro
def spinLeft():
    initio.spinLeft(100)
    
@webiopi.macro
def spinRight():
    initio.spinRight(100)
    
@webiopi.macro
def forwardLeft():
    initio.turnForward(10, 100)
    
@webiopi.macro
def forwardRight():
    initio.turnForward(100, 10)
    
@webiopi.macro
def reverseLeft():
    initio.turnReverse(10, 100)
    
@webiopi.macro
def reverseRight():
    initio.turnReverse(100, 10)
