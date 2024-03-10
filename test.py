import re

class ConfigValidator:
    @staticmethod
    def is_valid(username, password, broker_address, port, topic):
        # Checke ob es leer ist
        if not (username and password and broker_address and port and topic):
            return False
        # broker port
        if not str(port).isdigit():
            return False
        # Checke topic
        if not re.search(r'[#/]', topic):
            print('ja')
            return False

        return True


# Beispielaufruf
validator = ConfigValidator()
print(validator.is_valid("testtest", "Test1234", "4757e0b60f564e78900a097c3086a003.s1.eu.hivemq.cloud", 8883, "#todoapptasks"))  # True