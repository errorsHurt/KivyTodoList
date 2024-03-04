import time

from kivy.uix.screenmanager import Screen
from logic.storage.TaskStorageHandler import TaskStorageHandler
import uuid as UUID


class MainToDoList(Screen):

    def __init__(self, mqtt_client, **kw):
        super().__init__(**kw)
        self.mqtt_client = mqtt_client

    def foobar(self):
        self.mqtt_thread.start_mqtt_thread()
        self.mqtt_thread.wait_for_mqtt_thread()
        data = self.mqtt_client.get_retained_messages()

    def load_tasks_in_local_list(self, tasks):
        self.ids.rv.data = []
        for task in tasks:
            self.ids.rv.data.append({'id': str(task["uuid"]),
                                     'text': task["message"],
                                     'is_done': task["state"]})

    def add_item(self, uuid=""):

        if uuid == "":
            uuid = UUID.uuid4()  # Generate a unique ID

        text = 'New Task'
        # Explicitly set `is_done` to False for new items
        self.ids.rv.data.append({'id': str(uuid), 'text': text, 'is_done': False})
        self.ids.rv.refresh_from_data()
        # Wenn "+"

        TaskStorageHandler._add_task(str(self.mqtt_client.config.client_id), text)
        # MainToDoList.sync_items()
        data = TaskStorageHandler._read_data()
        self.mqtt_client.publish_message(str(data), True)

    def sync_items(self):
        # connect
        self.mqtt_client.client.subscribe(self.mqtt_client.config.topic, qos=self.mqtt_client.config.qos)
        self.mqtt_client.start_loop()
        time.sleep(2)
        self.mqtt_client.stop_loop()

        print('A')
        msg = self.mqtt_client.get_retained_messages()
        print(msg)
        if msg:
            print('B')
            TaskStorageHandler._write_data(msg)
            #data = TaskStorageHandler._read_data()
            #tasks = data["tasks"]
            tasks = msg["tasks"]
            self.load_tasks_in_local_list(tasks)

    def delete_item(self, task_uuid):
        # Hier müssen wir bevor das Item gelöscht wird die Sync Funktion aufrufen und dann das Item Löschen.
        # Wir haben ja davor schon die Funktion eingebaut das wir erst mal checken ob das item überhaupt enthalten ist
        # Somit dürfte das eigentlich kein problem darstellen.
        # Später können wir theoretisch einfach den Thread über die "sync_items" funktion rüber laufen lassen.

        #MainToDoList.sync_items()
        TaskStorageHandler._delete_task(task_uuid)

        self.ids.rv.data = [item for item in self.ids.rv.data if item['id'] != task_uuid]

        data = TaskStorageHandler._read_data()
        tasks = data["tasks"]
        self.load_tasks_in_local_list(tasks)

        data = TaskStorageHandler._read_data()
        self.mqtt_client.publish_message(str(data), True)

    def edit_item(self, item_widget):
        # Trigger editing using the item's widget but reference by ID
        self.selected_item_id = item_widget.id  # Store the selected item's ID
        self.ids.global_edit_text.text = item_widget.text
        self.ids.global_edit_text.disabled = False
        self.ids.global_edit_text.opacity = 1
        self.ids.global_edit_text.focus = True
        # 1. Das Item mit der UUID finden und in der .json auch umbenennen.
        # 2. Liste neu laden und Publicchhhen

        #MainToDoList.sync_items()
        TaskStorageHandler._edit_task(self.selected_item_id, txt=self.ids.global_edit_text.text)
        data = TaskStorageHandler._read_data()
        self.mqtt_client.publish_message(str(data), True)

    def apply_global_edit(self):
        new_text = self.ids.global_edit_text.text
        # Update the item by ID
        for item in self.ids.rv.data:
            if item['id'] == self.selected_item_id:
                item['text'] = new_text
                break
        self.ids.rv.refresh_from_data()
        # Clear and hide the global TextInput
        self.ids.global_edit_text.text = ''
        self.ids.global_edit_text.opacity = 0
        self.ids.global_edit_text.disabled = True
        self.selected_item_id = None
