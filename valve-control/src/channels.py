from src.channel import Channel


class Channels:
    def __init__(self, bus, log, mqtt):
        self.counter = 0
        self.channelList = [Channel(nb, bus, log, mqtt) for nb in range(10)]

    def update(self):
        self.counter = (self.counter + 1) % Channel.COUNTER_CYCLE
        [self.channelList[nb].computeState((self.counter + Channel.NON_OVERLAP_TIME * nb) % Channel.COUNTER_CYCLE)
         for nb in range(10)]
