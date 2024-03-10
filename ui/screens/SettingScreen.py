from kivy.uix.screenmanager import Screen
from logic.mqtt.MqttConfig import MqttConfig
import re
class LoginScreen(Screen):

    def __init__(self, mqtt_client,**kw):
        super().__init__(**kw)
        self.mqtt_client = mqtt_client


    def is_valid(self, username, password, broker_adress, port, topic):
        # Validierung implementieren
        # Checke ob es leer ist
        if not (username and password and broker_adress and port and topic):
            return False
        # broker port
        if not str(port).isdigit():
            return False
        # Checke topic
        if not re.search(r'[#/]', topic):
            print('ja')
            return False

        return True

    def update_config_yaml(self, username_input, password_input, broker_adress_input, port_input, topic_input):
        print(self.is_valid(username_input, password_input, broker_adress_input, port_input, topic_input))

        if self.is_valid(username_input, password_input, broker_adress_input, port_input, topic_input):

            mqtt_config = {
                "mqtt": {
                    "client-id": "703601b0-cc92-4826-b06a-2fe3d034b502",
                    "connection": {
                        "broker-adress": broker_adress_input,
                        "port": port_input,
                        "qos": 1,
                        "topic": topic_input
                    },
                    "user": {
                        "password": username_input,
                        "username": password_input
                    }
                }
            }

            MqttConfig.write(mqtt_config)

        else:
            print("Es stehen keine Configs bereit")

