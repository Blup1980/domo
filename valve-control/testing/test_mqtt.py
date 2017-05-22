from unittest import TestCase
from unittest.mock import MagicMock, patch
import logging
mymodule_mqtt = MagicMock()
patch.dict("sys.modules", {'paho': mymodule_mqtt}).start()
patch.dict("sys.modules", {'paho.mqtt': mymodule_mqtt}).start()
patch.dict("sys.modules", {'paho.mqtt.client': mymodule_mqtt}).start()
from mqtt import MQTT


class TestMqtt(TestCase):
    def setUp(self):
        self.mock_log = logging.getLogger(__name__)
        self.mock_log.info = MagicMock()

    def test_connection(self):
        dut = MQTT(self.mock_log)
        dut.client.connect.assert_called_with("mosquitto", 1883, 60)

    def test_callBack_on_connect(self):
        expected_subscription = {("domo/valve/0/command", 0),
                                 ("domo/valve/1/command", 0),
                                 ("domo/valve/2/command", 0),
                                 ("domo/valve/3/command", 0),
                                 ("domo/valve/4/command", 0),
                                 ("domo/valve/5/command", 0),
                                 ("domo/valve/6/command", 0),
                                 ("domo/valve/7/command", 0),
                                 ("domo/valve/8/command", 0),
                                 ("domo/valve/9/command", 0)}
        dut = MQTT(self.mock_log)
        dut.client.on_connect(dut.client, None, None, None)
        subscribe_call_args = dut.client.subscribe.call_args[0]
        calls = set(subscribe_call_args[0])
        self.assertEquals(expected_subscription, calls)
