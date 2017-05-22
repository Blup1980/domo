from unittest import TestCase
from unittest.mock import MagicMock, patch
from channel import Channel
import logging

mymodule_mqtt = MagicMock()
mymodule_smbus = MagicMock()
patch.dict("sys.modules", {'paho': mymodule_mqtt}).start()
patch.dict("sys.modules", {'paho.mqtt': mymodule_mqtt}).start()
patch.dict("sys.modules", {'paho.mqtt.client': mymodule_mqtt}).start()
patch.dict("sys.modules", {'smbus': mymodule_smbus}).start()
from mqtt import MQTT
from i2cbus import I2cBus


class TestChannel(TestCase):
    def setUp(self):
        self.mock_log = logging.getLogger(__name__)
        self.mock_log.info = MagicMock()
        self.mqtt = MQTT(self.mock_log)
        self.mqtt.register_inbound_callback = MagicMock()
        self.mqtt.publish = MagicMock()
        self.bus = I2cBus(self.mock_log)
        self.bus.write = MagicMock()

    def test_registerCallback(self):
        channelNb = 2
        dut = Channel(channelNb, self.bus, self.mock_log, self.mqtt)
        self.mqtt.register_inbound_callback.assert_called_with(channelNb, dut.setPercent)

    def test_update_at_counter_value(self):
        channelNb = 2
        dut = Channel(channelNb, self.bus, self.mock_log, self.mqtt)

        # update to output waits counter == 0 to take new value when OFF to ON
        dut.setPercent(100)
        dut.computeState(1)
        self.mqtt.publish.assert_called_with(channelNb, False)
        self.bus.write.assert_called_with(channelNb, False)
        dut.computeState(0)
        self.mqtt.publish.assert_called_with(channelNb, True)
        self.bus.write.assert_called_with(channelNb, True)

        # update to output takes new value regardless of counter when ON to OFF
        dut.setPercent(0)
        self.mqtt.publish.assert_called_with(channelNb, True)
        self.bus.write.assert_called_with(channelNb, True)
        dut.computeState(1)
        self.mqtt.publish.assert_called_with(channelNb, False)
        self.bus.write.assert_called_with(channelNb, False)
        dut.setPercent(0)
        self.mqtt.publish.assert_called_with(channelNb, False)
        self.bus.write.assert_called_with(channelNb, False)

    def test_correct_percentage_ratio(self):
        channelNb = 0
        dut = Channel(channelNb, self.bus, self.mock_log, self.mqtt)

        percent = 0
        dut.setPercent(percent)
        for counter in range(Channel.COUNTER_CYCLE):
            dut.computeState(counter)
            self.mqtt.publish.assert_called_with(channelNb, False)
            self.bus.write.assert_called_with(channelNb, False)

        percent = 100
        dut.setPercent(percent)
        for counter in range(Channel.COUNTER_CYCLE):
            dut.computeState(counter)
            self.mqtt.publish.assert_called_with(channelNb, True)
            self.bus.write.assert_called_with(channelNb, True)

        percent = 50
        dut.setPercent(percent)
        for counter in range(Channel.COUNTER_CYCLE):
            dut.computeState(counter)
            expected_state = percent > (counter*100/Channel.COUNTER_CYCLE)
            self.mqtt.publish.assert_called_with(channelNb, expected_state)
            self.bus.write.assert_called_with(channelNb, expected_state)
