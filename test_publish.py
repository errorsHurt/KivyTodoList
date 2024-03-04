from logic.mqtt.MqttHandler import MqttHandler
from logic.mqtt.MqttThreadManager import MqttThreadManager
from logic.mqtt.MqttConfig import MqttConfig

if __name__ == "__main__":
    config = MqttConfig.load_from_resource()
    mqtt_client = MqttHandler(config)

    mqtt_client.client.connect(config.broker_adress, config.port)

    data = \
        {
            "tasks": [
                {"uuid": "044996fb-8183-406e-8eab-423838b67a71",
                 "client-id": "e4947a81-dbc2-40de-aad8-0dd3eab591f0",
                 "message": "TaskState Test",
                 "state": True
                 }
            ]
        }

    mqtt_client.publish_message(str(data), True)
