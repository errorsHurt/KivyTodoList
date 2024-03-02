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
            with open(tasks_data_path, "r") as read_file:
                data = json.load(read_file)

                tasks = data["tasks"]

                for index, task in enumerate(tasks):

                    if task.get('uuid') == uuid:
                        task['state'] = state
                        with open(tasks_data_path, "w") as write_file:
                            json.dump(data, write_file, indent=4)
                            write_file.close()
                read_file.close()


        except Exception as e:
            print(f"Status des Task konnte nicht aktuallisert werden:", uuid, state, e)

    """
                for index, task in enumerate(tasks):

                    if task.get('uuid') == uuid:
                        UPDATE
                        data["tasks"] = tasks  # Aktualisieren der Aufgabenliste in den Daten
    """


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

    @staticmethod
    def _read_data(as_string: bool = False):
        with open(tasks_data_path, "r") as file:
            if as_string:
                return str(json.load(file))
            return json.load(file)

    def _delete_task(uuid):
        with open(tasks_data_path, "r") as read_file:
            data = json.load(read_file)

            tasks = data.get("tasks", [])  # Holen der Liste von Aufgaben aus den Daten

            for index, task in enumerate(tasks):

                if task.get('uuid') == uuid:
                    del tasks[index]
                    data["tasks"] = tasks  # Aktualisieren der Aufgabenliste in den Daten
                    with open(tasks_data_path, "w") as write_file:
                        json.dump(data, write_file, indent=4)
                        write_file.close()
            read_file.close()


