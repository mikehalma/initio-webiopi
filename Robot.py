import webiopi

class Robot(object):

    def __init__(self):
        webiopi.setDebug()
        webiopi.debug('The test robot has been activated')

    def destroy(self):
        webiopi.debug('The test robot has been destoyed')

    def irStatus(self):
        webiopi.debug('The robot would sense stuff, if only it had some IR sensors')

    def forward(self):
        webiopi.debug('The robot would go forward, if only it had some wheels')

    def stop(self):
        webiopi.debug("The robot would stop, if only it had some whee... OK it's stopped")

    def reverse(self):
        webiopi.debug('The robot would reverse, if only it had some wheels')

    def spinLeft(self):
        webiopi.debug('The robot would spin left, if only it had some wheels')

    def spinRight(self):
        webiopi.debug('The robot would spin right, if only it had some wheels')

    def forwardLeft(self):
        webiopi.debug('The robot would go forward left, if only it had some wheels')

    def forwardRight(self):
        webiopi.debug('The robot would go forward right, if only it had some wheels')

    def reverseLeft(self):
        webiopi.debug('The robot would reverse left, if only it had some wheels')

    def reverseRight(self):
        webiopi.debug('The robot would reverse right, if only it had some wheels')
