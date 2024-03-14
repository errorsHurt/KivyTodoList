from logic.mqtt.MqttHandler import MqttHandler
from logic.mqtt.MqttConfig import MqttConfig

if __name__ == "__main__":

    config = MqttConfig.load_from_resource()
    mqtt_client = MqttHandler(config)

    mqtt_client.client.connect(config.broker_adress, config.port)

    retained_messages = mqtt_client.get_retained_messages()

    print("Aktuelle Nachrichten:", retained_messages)