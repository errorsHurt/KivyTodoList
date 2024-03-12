import random
import ssl
import threading

from paho.mqtt import client as mqtt_client


broker = '4757e0b60f564e78900a097c3086a003.s1.eu.hivemq.cloud'
port = 8883
topic = "todoapp/tasks"
# generate client ID with sub prefix randomly
client_id = f'python-mqtt-sub-{random.randint(0, 1000)}'
username = 'testtest'
password = 'Test1234'

message_received = threading.Event()

def connect_mqtt():
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


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    client.disconnect()
    message_received.set()  # Setze das Event, um das Skript zu beenden

def run():
    client = connect_mqtt()
    client.on_message = on_message
    client.loop_start()
    message_received.wait()  # Warte auf das Event, das vom on_message gesetzt wird
    client.loop_stop()
    client.disconnect()


if __name__ == '__main__':
    run()
