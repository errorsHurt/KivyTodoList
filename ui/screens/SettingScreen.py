from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

    def connect(self, username_input, password_input, topic_input):
        self.mqtt_client.client.connect(self.mqtt_client.config.broker_adress, self.mqtt_client.config.port)

        username = username_input
        password = password_input
        topic = topic_input
