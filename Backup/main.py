from mqtt.MqttHandler import MqttClient
from mqtt.MqttThreadManager import MqttThreadManager
from mqtt.MqttConfig import MqttConfig

if __name__ == "__main__":

    config = MqttConfig("resources/config.yaml")
    mqtt_client = MqttClient(config)

    mqtt_thread_manager = MqttThreadManager(mqtt_client)
    mqtt_thread_manager.start_mqtt_thread()
    mqtt_thread_manager.wait_for_mqtt_thread()

    retained_messages = mqtt_client.get_retained_messages()
    print("Aktuelle Nachrichten:", retained_messages)