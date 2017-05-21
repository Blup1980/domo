#!/usr/bin/python3
import logging

from gi.repository import GObject
from channels import Channels
from i2cbus import I2cBus

from mqtt import MQTT

MILI_IN_SEC = 1000
UPDATE_RATE_SEC = 60


def timerEvent():
    logging.info('Running timer event')
    channels.update()
    logging.info('End of timer event')
    return True


# init things
loop = GObject.MainLoop()

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='/valve/log/channel.log',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('Script started')

i2c = I2cBus(logger)
mqtt = MQTT(logger)
channels = Channels(i2c,logger,mqtt)

timer = GObject.timeout_add(MILI_IN_SEC*UPDATE_RATE_SEC, timerEvent)

mqtt.startThread()
loop.run()
