
class Channel:
    COUNTER_CYCLE = 30
    NON_OVERLAP_TIME = 3

    def __init__(self, channel, bus, log, mqtt):
        self.channelNb = channel
        self.bus = bus
        self.log = log
        self.mqtt = mqtt
        self.threshold = 0
        self.newThreshold = 0
        self.valveOpen = False
        mqtt.register_inbound_callback(self.channelNb, self.setPercent)

    def setPercent(self, percent):
        if percent > 100:
            percent = 100
        if percent < 0:
            percent = 0
        self.newThreshold = percent*Channel.COUNTER_CYCLE/100
        if self.newThreshold < self.threshold:
            self.threshold = self.newThreshold
        self.log.info("Chan=" + str(self.channelNb) + " set to " + str(percent))

    def computeState(self, cntr):
        if cntr == 0:
            self.threshold = self.newThreshold
        newValveState = cntr < self.threshold
        self.valveOpen = newValveState
        self.mqtt.publish(self.channelNb,self.valveOpen)
        self.bus.write(self.channelNb, self.valveOpen)
