import time
import paho.mqtt.client as paho
from paho import mqtt
from logic.mqtt.MqttConfig import MqttConfig

class MqttHandler:

    def __init__(self, config: MqttConfig):
        self.config = config

        self.topic = config.topic

        self.__retainedMessages = []

        self.client = paho.Client(paho.CallbackAPIVersion.VERSION1, client_id=config.client_id, userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.on_connect

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(config.username, config.password)

        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        self.client.subscribe(self.topic, qos=config.qos)
        self.received_message = None  # Variable zum Speichern der empfangenen Nachricht

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connection received with code %s." % rc)
        pass

    def on_publish(self, client, userdata, mid, properties=None):
        print("Published: " + str(mid))
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " [%s]" % granted_qos)
        pass

    def on_message(self, client, userdata, msg):
        print(client, userdata, msg)
        self.__retainedMessages.append(msg.payload.decode("utf-8"))
        print(msg.topic + " - " + str(msg.payload))

    def publish_message(self, message, retain=False, qos=1):
        self.__delete_old_retained_messages()
        time.sleep(1)
        self.client.connect(self.config.broker_adress, self.config.port)
        time.sleep(0.5)
        self.client.publish(self.topic, payload=str(message), qos=qos, retain=retain)
        self.client.disconnect()

    def start_loop(self):
        self.client.connect(self.config.broker_adress, self.config.port)
        self.client.loop_start()

    def stop_loop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def get_retained_messages(self):

        self.client.connect(self.config.broker_adress, self.config.port)
        self.client.subscribe(self.config.topic, self.config.qos)
        time.sleep(0.5)
        self.client.loop_start()

        time.sleep(0.5)

        self.client.loop_stop()

        self.client.disconnect()

        retained_messages = self.__retainedMessages.copy()
        self.__retainedMessages.clear()

        return retained_messages

    def __delete_old_retained_messages(self):
        self.client.connect(self.config.broker_adress, self.config.port)
        time.sleep(0.5)
        self.client.publish(self.topic, payload=None, qos=0, retain=True)

