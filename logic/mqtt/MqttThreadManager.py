import threading
import time


class MqttThreadManager:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.mqtt_thread = None

    def start_mqtt_thread(self):
        self.mqtt_thread = threading.Thread(target=self._mqtt_worker)
        self.mqtt_thread.start()

    def wait_for_mqtt_thread(self):
        if self.mqtt_thread:
            self.mqtt_thread.join()

    def _mqtt_worker(self):
        self.mqtt_client.start_loop()
        time.sleep(10)
        self.mqtt_client.stop_loop()