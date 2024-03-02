import json
import uuid

tasks_data_path = "resources/tasks.json"


class TaskStorageHandler:

    def __init__(self):
        pass

    @staticmethod
    def _add_task(client_id, message):
        task_uuid = uuid.uuid4()
        client_id = client_id
        message = message
        state = False

        TaskStorageHandler.__write(task_uuid, client_id, message, state)

    @staticmethod
    def _set_task_state(uuid, state: bool):
        try:
            file = TaskStorageHandler._read_file()
            data = json.load(file)

            if TaskStorageHandler.__task_exists(uuid, data["tasks"]):
                TaskStorageHandler.__update_task_state(uuid, state)

        except Exception as e:
            print(f"Status des Task konnte nicht aktuallisert werden:", uuid, state, e)

    @staticmethod
    def _read_file():
        return open(tasks_data_path)

    @staticmethod
    def __task_exists(uuid, elements):

        for element in elements:
            if element["uuid"] == uuid:
                return True
        return False

    @staticmethod
    def __update_task_state(uuid, state: bool):

        try:
            with open(tasks_data_path, "r") as file:
                data = json.load(file)

                data["tasks"][uuid]["state"] = state

                TaskStorageHandler._write_data(data)
                file.close()

        except Exception as e:
            print("Es ist ein Fehler beim aktualisieren der Datei aufgetreten:", uuid, state, e)

    @staticmethod
    def __write(task_uuid, client_id, message, state):
        try:
            with open(tasks_data_path, "r") as file:
                data = json.load(file)

                task: dict = {
                    "uuid": str(task_uuid),
                    "client-id": str(client_id),
                    "message": message,
                    "state": state
                }

                data["tasks"].append(task)

                TaskStorageHandler._write_data(data)

                file.close()

        except Exception as e:
            print("Es ist ein Fehler beim schreiben der Datei aufgetreten:", state, e)

    @staticmethod
    def _write_data(data):
        with open(tasks_data_path, "w") as file:
            json.dump(data, file, indent=4)
            file.close()
