from unittest import TestCase
from unittest.mock import MagicMock
from channel import Channel
from channels import Channels
import logging


class MockMQTT:
    def __init__(self, log):
        pass

    def register_inbound_callback(self, channelNb, functionPtr):
        pass

    def publish(self, channelNb, data):
        pass


class MockI2cBus:
    def write(self, valve_nb, state):
        pass


class TestChannels(TestCase):
    def setUp(self):
        self.mock_mqtt = MockMQTT
        self.mock_mqtt.register_inbound_callback = MagicMock()
        self.mock_mqtt.publish = MagicMock()
        self.mock_log = logging.getLogger(__name__)
        self.mock_log.info = MagicMock()
        self.mock_bus = MockI2cBus
        self.mock_bus.write = MagicMock()

    def test_channel_created(self):
        dut = Channels(self.mock_bus, self.mock_log, self.mock_mqtt)

        for c in dut.channelList:
            self.assertIsInstance(c, Channel)

    def test_shifted_starts(self):
        dut = Channels(self.mock_bus, self.mock_log, self.mock_mqtt)
        valveState = [False]*10

        # all a 100%
        for c in dut.channelList:
            c.setPercent(100)

        for counter in range(Channel.COUNTER_CYCLE):
            dut.update()
            for c in dut.channelList:
                c.setPercent(100)
            newValveState = [c.valveOpen for c in dut.channelList]
            changedValveState = zip(newValveState, valveState)

            changed = False
            for pair in changedValveState:
                if pair[0] != pair[1]:
                    self.assertFalse(changed)
                    changed = True

            valveState = newValveState
