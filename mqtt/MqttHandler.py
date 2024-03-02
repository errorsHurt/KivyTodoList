import time

import paho.mqtt.client as paho
from paho import mqtt
from mqtt.MqttConfig import MqttConfig


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



    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connection received with code %s." % rc)

    def on_publish(self, client, userdata, mid, properties=None):
        print("Published: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " [%s]" % granted_qos)

    def on_message(self, client, userdata, msg):
        self.__retainedMessages.append(msg.payload)
        print(msg.topic + " - " + str(msg.payload))

    def publish_message(self, message, retain=False, qos=1):
        self.__delete_old_retained_messages()
        
        self.client.connect(self.config.broker_adress, self.config.port)
        time.sleep(0.5)
        self.client.publish(self.topic, payload=message, qos=qos, retain=retain)
        
        

    def start_loop(self):
        self.client.loop_start()

    def stop_loop(self):
        self.client.loop_stop()

    def loop(self, timeout=5):
        self.client.loop(timeout)

    def get_retained_messages(self):
        return self.__retainedMessages.copy()

    #TODO
    def __delete_old_retained_messages(self):
        self.client.connect(self.config.broker_adress, self.config.port)
        time.sleep(0.5)
        self.client.publish(self.topic, payload="", qos=0, retain=True)
