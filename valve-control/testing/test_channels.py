from unittest import TestCase
from unittest.mock import MagicMock, patch
from channel import Channel
from channels import Channels
import logging

mymodule_mqtt = MagicMock()
mymodule_smbus = MagicMock()
patch.dict("sys.modules", {'paho': mymodule_mqtt}).start()
patch.dict("sys.modules", {'paho.mqtt': mymodule_mqtt}).start()
patch.dict("sys.modules", {'paho.mqtt.client': mymodule_mqtt}).start()
patch.dict("sys.modules", {'smbus': mymodule_smbus}).start()
from mqtt import MQTT
from i2cbus import I2cBus


class TestChannels(TestCase):
    def setUp(self):
        self.mock_log = logging.getLogger(__name__)
        self.mock_log.info = MagicMock()
        self.mqtt = MQTT(self.mock_log)
        self.mqtt.register_inbound_callback = MagicMock()
        self.mqtt.publish = MagicMock()
        self.bus = I2cBus(self.mock_log)

    def test_channel_created(self):
        dut = Channels(self.bus, self.mock_log, self.mqtt)

        for c in dut.channelList:
            self.assertIsInstance(c, Channel)

    def test_shifted_starts(self):
        dut = Channels(self.bus, self.mock_log, self.mqtt)
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
