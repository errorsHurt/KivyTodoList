from kivy.uix.screenmanager import Screen
from logic.mqtt.MqttConfig import MqttConfig
class LoginScreen(Screen):

    def __init__(self, mqtt_client,**kw):
        super().__init__(**kw)
        self.mqtt_client = mqtt_client

    def update_config_yaml(self, username_input, password_input, broker_adress_input, port_input, topic_input):

        data = MqttConfig.read()

        data['mqtt']['connection']['broker-adress'] = broker_adress_input
        data['mqtt']['port'] = port_input
        data['mqtt']['topic'] = topic_input
        data['mqtt']['user']['username'] = username_input
        data['mqtt']['user']['password'] = password_input

        #MqttConfig.write(data)
