from kivy.uix.screenmanager import Screen
from logic.mqtt.MqttConfig import MqttConfig
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import re
import sys
class LoginScreen(Screen):

    def __init__(self, mqtt_client,**kw):
        super().__init__(**kw)
        self.mqtt_client = mqtt_client


    def is_valid(self, username, password, broker_adress, port, topic):
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
        username_input = username_input.text
        password_input = password_input.text
        broker_adress_input = broker_adress_input.text
        port_input = port_input.text
        topic_input = topic_input.text
        print(self.is_valid(username_input, password_input, broker_adress_input, port_input, topic_input))

        if self.is_valid(username_input, password_input, broker_adress_input, port_input, topic_input):

            mqtt_config = {
                "mqtt": {
                    "client-id": "703601b0-cc92-4826-b06a-2fe3d034b502",
                    "connection": {
                        "broker-adress": broker_adress_input,
                        "port": int(port_input),
                        "qos": 1,
                        "topic": topic_input
                    },
                    "user": {
                        "username": username_input,
                        "password": password_input
                    }
                }
            }

            MqttConfig.write(mqtt_config)
            self.show_shutdown_dialog()
        else:
            print("Es stehen keine Configs bereit")

    def show_shutdown_dialog(self):
        # Ensure only one instance of the dialog is created
        if not hasattr(self, 'shutdown_dialog'):
            self.shutdown_dialog = MDDialog(
                title="Neustart Benachrichtung",
                text="Bitte starten sie die App neu.",
                buttons=[
                    MDFlatButton(
                        text="Okay",
                        on_release=self.shutdown_app
                    ),
                ],
            )
        self.shutdown_dialog.open()

    def shutdown_app(self, *args):
        self.shutdown_dialog.dismiss()
        sys.exit()