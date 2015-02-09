import webiopi
import json

# The base robot implementation as expected by the web application.
# By extending this class, you can implement only the parts of the
# interface that your robot supports.
# This class can be used to test the web application.
class Robot(object):

    def __init__(self):
        webiopi.setDebug()
        webiopi.debug('The test robot has been activated')

    def destroy(self):
        webiopi.debug('The test robot has been destoyed')

    def irStatus(self):
        webiopi.debug('I would sense stuff, if only I had some IR sensors')
        return ''
        status = {}
        status["notFound"] = True
        return json.dumps(status)

    def forward(self):
        webiopi.debug('I would go forward, if only I had some wheels')

    def stop(self):
        webiopi.debug("I would stop, if only I had some whee... OK I've stopped")

    def reverse(self):
        webiopi.debug('I would reverse, if only I had some wheels')

    def spinLeft(self):
        webiopi.debug('I would spin left, if only I had some wheels')

    def spinRight(self):
        webiopi.debug('I would spin right, if only I had some wheels')

    def forwardLeft(self):
        webiopi.debug('I would go forward left, if only I had some wheels')

    def forwardRight(self):
        webiopi.debug('I would go forward right, if only I had some wheels')

    def reverseLeft(self):
        webiopi.debug('I would reverse left, if only I had some wheels')

    def reverseRight(self):
        webiopi.debug('I would reverse right, if only I had some wheels')
