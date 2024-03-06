import threading
import time
import json
import paho.mqtt.client as paho
from paho import mqtt
from logic.mqtt.MqttConfig import MqttConfig
from paho.mqtt import client as mqtt_client
import ssl
import random

# NEW
broker = '4757e0b60f564e78900a097c3086a003.s1.eu.hivemq.cloud'
port = 8883
topic = "todoapp/tasks"
# generate client ID with sub prefix randomly
client_id = f'python-mqtt-sub-{random.randint(0, 1000)}'
username = 'testtest'
password = 'Test1234'
message_received = threading.Event()


class MqttHandler:

    def __init__(self, config: MqttConfig):
        self.config = config

        self.topic = config.topic

        self.__retainedMessages = []

        self.client = paho.Client(client_id=config.client_id, userdata=None, protocol=paho.MQTTv5)
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

    def on_publish(self, client, userdata, mid, properties=None):
        print("Published: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " [%s]" % granted_qos)

    def on_message(self, client, userdata, msg):
        self.__retainedMessages.append(json.loads(msg.payload.decode("utf-8")))
        print(msg.topic + " - " + str(msg.payload))

    def publish_message(self, message, retain=False, qos=1):
        self.__delete_old_retained_messages()

        self.client.connect(self.config.broker_adress, self.config.port)
        time.sleep(0.5)
        self.client.publish(self.topic, payload=message, qos=qos, retain=retain)
        self.client.disconnect()

    def start_loop(self):
        self.client.connect(self.config.broker_adress, self.config.port)
        self.client.loop_start()

    def stop_loop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def loop(self, timeout=5):
        self.client.loop(timeout)

    def get_retained_messages(self):
        return self.__retainedMessages.copy()

    # TODO
    def __delete_old_retained_messages(self):
        self.client.connect(self.config.broker_adress, self.config.port)
        time.sleep(0.5)
        self.client.publish(self.topic, payload="", qos=0, retain=True)

    # New
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                client.subscribe(topic)
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)

        # Set TLS parameters
        client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLS)

        client.on_connect = on_connect
        client.connect(broker, port)
        return client

    def on_message(self, client, userdata, msg):
        # print(f"Received message: {msg.payload.decode()}")
        self.received_message = msg.payload.decode()  # Speichern der empfangenen Nachricht
        client.disconnect()
        message_received.set()

    def lissen(self):
        client = self.connect_mqtt()
        client.on_message = self.on_message
        client.loop_start()
        message_received.wait()
        client.loop_stop()
        client.disconnect()
        return self.received_message
