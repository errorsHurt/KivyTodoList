from logic.mqtt.MqttHandler import MqttHandler
from logic.mqtt.MqttThreadManager import MqttThreadManager
from logic.mqtt.MqttConfig import MqttConfig

if __name__ == "__main__":

    config = MqttConfig.load_from_resource()
    mqtt_client = MqttHandler(config)

    mqtt_client.client.connect(config.broker_adress, config.port)

    mqtt_thread_manager = MqttThreadManager(mqtt_client)
    mqtt_thread_manager.start_mqtt_thread()
    mqtt_thread_manager.wait_for_mqtt_thread()

    retained_messages = mqtt_client.get_retained_messages()
    print("Aktuelle Nachrichten:", retained_messages)