import re
import paho.mqtt.client as mqtt

re_channel = re.compile('domo/valve/(\d+)/command')


class MQTT:
    inbound_callbacks = [None]*10
    log = None

    def __init__(self, log):
        MQTT.log = log
        try:
            self.client = mqtt.Client()
            self.client.on_connect = MQTT._on_connect
            self.client.on_message = MQTT._on_message
            self.client.connect("mosquitto", 1883, 60)

        except:
            self.log.error('Error while accessing mqtt')
            exit()

    def _on_connect(client, userdata, flags, rc):
        client.subscribe([("domo/valve/2/command",0)])
        MQTT.log.info('MQTT on connect called')

    def _on_message(client, userdata, msg):
        match = re_channel.match(msg.topic)
        channelNb = int(match.group(1))
        percent = 0
        if msg.payload == b'ON':
            percent = 100
        MQTT.log.info('MQTT message: Channel ' + str(channelNb) + " Command " + str(percent))
        MQTT.inbound_callbacks[channelNb](percent)

    def register_inbound_callback(self, channelNb, functionPtr):
        MQTT.inbound_callbacks[channelNb] = functionPtr

    def startThread(self):
        self.client.loop_start()

    def publish(self, channelNb, data):
        if data:
            msg = b'OPEN'
        else:
            msg = b'CLOSED'
        MQTT.log.info('MQTT Publishing: Script started /domo/valve/' + str(channelNb)
                      + '/status with payload :' + str(msg))
        self.client.publish('/domo/valve/' + str(channelNb) + '/status', payload=msg, qos=0, retain=True)
