import time
import json
from kivy.uix.screenmanager import Screen
from logic.storage.TaskStorageHandler import TaskStorageHandler
import uuid as UUID


class MainScreen(Screen):

    def __init__(self, mqtt_client, **kw):
        super().__init__(**kw)
        self.mqtt_client = mqtt_client

    def load_tasks_in_local_list(self, tasks):
        data = []
        for task in tasks:
            item = {'id': str(task["uuid"]), 'text': task["message"], 'state': task["state"]}
            data.append(item)
        self.ids.rv.data = data

    def add_item(self, uuid=""):
        if uuid == "":
            # Das hier hatte gefehlt
            # Hatten nen falschen Datentyp
            uuid = str(UUID.uuid4())

        text = 'New Task'
        new_item = {'id': uuid, 'text': text, 'state': False}
        self.ids.rv.data.append(new_item)
        self.ids.rv.refresh_from_data()
        TaskStorageHandler._add_task(str(self.mqtt_client.config.client_id), text)
        data = TaskStorageHandler._read_data()
        self.mqtt_client.publish_message(data, True)

    def sync_items(self):
        data = self.mqtt_client.lissen()
        print(data)
        if data:
            try:
                data = data.replace("'", "\"").replace("True", "true").replace("False", "false")
                data = json.loads(data)
                TaskStorageHandler._write_data(data)
                self.load_tasks_in_local_list(data["tasks"])

            except json.JSONDecodeError as e:
                print("Fehler:", e)

    def delete_item(self, task_uuid):

        TaskStorageHandler._delete_task(task_uuid)

        self.ids.rv.data = [item for item in self.ids.rv.data if item['id'] != task_uuid]

        data = TaskStorageHandler._read_data()
        tasks = data["tasks"]
        self.load_tasks_in_local_list(tasks)

        self.mqtt_client.publish_message(data, True)

    def edit_item(self, item_widget):
        # Trigger editing using the item's widget but reference by ID
        self.selected_item_id = item_widget.id  # Store the selected item's ID
        self.ids.global_edit_text.text = item_widget.text
        self.ids.global_edit_text.disabled = False
        self.ids.global_edit_text.opacity = 1
        self.ids.global_edit_text.focus = True

        #self.sync_items()

    def apply_global_edit(self):
        new_text = self.ids.global_edit_text.text
        # Update the item by ID
        for item in self.ids.rv.data:
            if item['id'] == self.selected_item_id:
                item['text'] = new_text
                break

        self.ids.rv.refresh_from_data()
        # Clear and hide the global TextInput
        TaskStorageHandler._edit_task(self.selected_item_id, txt=self.ids.global_edit_text.text)
        time.sleep(1)
        data = TaskStorageHandler._read_data()
        self.mqtt_client.publish_message(data, True)

        self.ids.global_edit_text.text = ''
        self.ids.global_edit_text.opacity = 0
        self.ids.global_edit_text.disabled = True
        self.selected_item_id = None




