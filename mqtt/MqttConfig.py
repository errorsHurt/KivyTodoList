import sys
import yaml


class MqttConfig:
    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)

                mqtt_config = data['mqtt']
                connection_config = mqtt_config['connection']
                user_config = mqtt_config['user']

                self.client_id = mqtt_config['client-id']
                self.broker_adress = connection_config['broker-adress']
                self.port = connection_config['port']
                self.topic = connection_config['topic']
                self.qos = connection_config['qos']
                self.username = user_config['username']
                self.password = user_config['password']

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e, data}.")
            sys.exit(1)