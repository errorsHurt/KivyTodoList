import json
import uuid

#tasks_data_path = "../tasks.json"
# Das hier MUSS so angegeben werden
tasks_data_path = "resources/tasks.json"


class TaskStorageHandler:

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
    def _read_data():
        try:
            with open(tasks_data_path, "r") as file:
                file.seek(0)
                return json.load(file)
        except Exception as e:
            print("Es ist ein Fehler aufgetreten:", e)

    @staticmethod
    def _write_data(data):
        with open(tasks_data_path, "w") as file:
            json.dump(data, file, indent=4)
            file.close()

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

    @staticmethod
    def _edit_task(uuid, txt):
        try:
            with open(tasks_data_path, "r") as read_file:
                data = json.load(read_file)
                tasks = data.get("tasks", [])
                for task in tasks:
                    if task.get('uuid') == uuid:
                        task['message'] = txt
                        break
                with open(tasks_data_path, "w") as write_file:
                    json.dump(data, write_file, indent=4)
        except Exception as e:
            print("Fehler beim Bearbeiten der Aufgabe:", e)