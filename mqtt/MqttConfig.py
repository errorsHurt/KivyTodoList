import sys
import yaml

class MqttConfig:

    def __init__(self, client_id, broker_adress, port, topic, qos, username, password):
        self.client_id = client_id
        self.broker_adress = broker_adress
        self.port = port
        self.topic = topic
        self.qos = qos
        self.username = username
        self.password = password

    @staticmethod
    def load_from_resource():
        file_path = 'resources/config.yaml'
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)

                mqtt_config = data['mqtt']
                connection_config = mqtt_config['connection']
                user_config = mqtt_config['user']

                client_id = mqtt_config['client-id']
                broker_adress = connection_config['broker-adress']
                port = connection_config['port']
                topic = connection_config['topic']
                qos = connection_config['qos']
                username = user_config['username']
                password = user_config['password']

                return MqttConfig(client_id,broker_adress,port,topic,qos,username,password)

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e, data}.")
            sys.exit(1)

    @staticmethod
    def write_to_yaml(path, value):
        # schreib dynamisch auf config.yaml
        pass