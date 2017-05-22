from unittest import TestCase
from unittest.mock import MagicMock
from channel import Channel
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


class TestChannel(TestCase):
    def setUp(self):
        self.mock_mqtt = MockMQTT
        self.mock_mqtt.register_inbound_callback = MagicMock()
        self.mock_mqtt.publish = MagicMock()
        self.mock_log = logging.getLogger(__name__)
        self.mock_log.info = MagicMock()
        self.mock_bus = MockI2cBus
        self.mock_bus.write = MagicMock()

    def test_registerCallback(self):
        channelNb = 2
        dut = Channel(channelNb, self.mock_bus, self.mock_log, self.mock_mqtt)
        self.mock_mqtt.register_inbound_callback.assert_called_with(channelNb, dut.setPercent)

    def test_update_at_counter_value(self):
        channelNb = 2
        dut = Channel(channelNb, self.mock_bus, self.mock_log, self.mock_mqtt)

        # update to output waits counter == 0 to take new value when OFF to ON
        dut.setPercent(100)
        dut.computeState(1)
        self.mock_mqtt.publish.assert_called_with(channelNb, False)
        self.mock_bus.write.assert_called_with(channelNb, False)
        dut.computeState(0)
        self.mock_mqtt.publish.assert_called_with(channelNb, True)
        self.mock_bus.write.assert_called_with(channelNb, True)

        # update to output takes new value regardless of counter when ON to OFF
        dut.setPercent(0)
        self.mock_mqtt.publish.assert_called_with(channelNb, True)
        self.mock_bus.write.assert_called_with(channelNb, True)
        dut.computeState(1)
        self.mock_mqtt.publish.assert_called_with(channelNb, False)
        self.mock_bus.write.assert_called_with(channelNb, False)
        dut.setPercent(0)
        self.mock_mqtt.publish.assert_called_with(channelNb, False)
        self.mock_bus.write.assert_called_with(channelNb, False)

    def test_correct_percentage_ratio(self):
        channelNb = 0
        dut = Channel(channelNb, self.mock_bus, self.mock_log, self.mock_mqtt)

        percent = 0
        dut.setPercent(percent)
        for counter in range(Channel.COUNTER_CYCLE):
            dut.computeState(counter)
            self.mock_mqtt.publish.assert_called_with(channelNb, False)
            self.mock_bus.write.assert_called_with(channelNb, False)

        percent = 100
        dut.setPercent(percent)
        for counter in range(Channel.COUNTER_CYCLE):
            dut.computeState(counter)
            self.mock_mqtt.publish.assert_called_with(channelNb, True)
            self.mock_bus.write.assert_called_with(channelNb, True)

        percent = 50
        dut.setPercent(percent)
        for counter in range(Channel.COUNTER_CYCLE):
            dut.computeState(counter)
            expected_state = percent > (counter*100/Channel.COUNTER_CYCLE)
            self.mock_mqtt.publish.assert_called_with(channelNb, expected_state)
            self.mock_bus.write.assert_called_with(channelNb, expected_state)
