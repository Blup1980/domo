#!/usr/bin/python3
import logging 
import time
import smbus
from gi.repository import GObject
import paho.mqtt.client as mqtt
import re

DEVICE_ADDRESS = 0x20
DEVICE_REG_IODIR0 = 0x06
DEVICE_REG_IODIR1 = 0x07
DEVICE_REG_GP0 = 0x00
DEVICE_REG_GP1 = 0x01

COUNTER_CYCLE = 30
NON_OVERLAP_TIME = 3


class Channel():
    portAssignement =  8* [DEVICE_REG_GP0] + 2*[DEVICE_REG_GP1]
    pinAssignement  =  [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01, 0x40, 0x80]
    currentPort = {DEVICE_REG_GP0 : 0x00, DEVICE_REG_GP1 : 0x00 }

    def __init__(self,channel,bus):
        self.channelNb = channel
        self.bus = bus
        self.myPort = self.portAssignement[self.channelNb]
        self.myPin = self.pinAssignement[self.channelNb]
        self.threshold = 0;
        self.newThreshold = 0;
        self.valveOpen = False;

    def setPercent(self, percent):
        if percent > 100:
            percent = 100
        if percent < 0:
            percent = 0
        self.newThreshold = percent*COUNTER_CYCLE/100
        if self.newThreshold < self.threshold:
            self.threshold = self.newThreshold
        logging.info("Chan=" + str(self.channelNb) + " set to " + str(self.threshold))

    def getPercent(self):
        return self.newThreshold*100/COUNTER_CYCLE

    def getValve(self):
        return self.valveOpen
    
    def _setOutput(self,value):
        if value == True:      
            self.currentPort[self.myPort] = self.currentPort[self.myPort] | self.myPin
        else:
            self.currentPort[self.myPort] = self.currentPort[self.myPort] & ~self.myPin
        self.bus.write_byte_data(DEVICE_ADDRESS, self.myPort,self.currentPort[self.myPort])

    def computeState(self,cntr):
        if cntr == 0:
            self.threshold = self.newThreshold
        newValveState = cntr < self.threshold
        self.valveOpen = newValveState
        if self.valveOpen == True:
           msg = b'OPEN'
        else:
           msg = b'CLOSED'
        logging.info('MQTT Publishing: Script started /domo/valve/' + str(self.channelNb) + '/status with payload :' + msg )
        client.publish('/domo/valve/' + str(self.channelNb) + '/status', payload=msg, qos=0, retain=False)
        self._setOutput( self.valveOpen)
    
def timerEvent():
    logging.info('Running timer event')
    global counter
    counter = (counter + 1)%COUNTER_CYCLE;
    [channelList[nb].computeState((counter+NON_OVERLAP_TIME*nb)%COUNTER_CYCLE) for nb in range(10)]
    logging.info('End of timer event')
    return True

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("domo/valve/2/command",0)])
    logging.info('MQTT on connect called')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    match = re_channel.match(msg.topic)
    channelNb = int(match.group(1))
    percent = 0
    if (msg.payload == b'ON'):
       percent = 100
    logging.info('MQTT message: Channel ' + str(channelNb) + " Command " + str(percent))
    channelList[channelNb].setPercent(percent)



# init things
counter = 0;
re_channel = re.compile('domo/valve/(\d+)/command')
loop = GObject.MainLoop()
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='/valve/log/channel.log', level=logging.DEBUG)
logging.info('Script started')
try:
    I2Cbus = smbus.SMBus(1)
    I2Cbus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_GP0, 0x00)
    I2Cbus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_GP1, 0x00)
    I2Cbus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_IODIR0, 0x00)
    I2Cbus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_IODIR1, 0x3F)
except:
    logging.error('Error while accessing i2c port')
    exit()

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mosquitto", 1883, 60)
except:
    logging.error('Error while accessing mqtt')
    exit()

channelList = [Channel(nb,I2Cbus) for nb in range(10)]

timer = GObject.timeout_add(1000*60, timerEvent)
client.loop_start()
loop.run()

