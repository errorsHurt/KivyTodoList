from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from storage.TaskStorageHandler import TaskStorageHandler
from mqtt.MqttHandler import MqttHandler
from mqtt.MqttConfig import MqttConfig
import uuid as UUID

Window.size = (310, 580)

config = MqttConfig.load_from_resource()
mqtt_client = MqttHandler(config)


class ToDoListItem(BoxLayout):
    checkbox = ObjectProperty(None)
    id = StringProperty('')
    text = StringProperty('')
    is_done = BooleanProperty(False)  # Keeps track of whether the task is done

    def __init__(self, **kwargs):
        super(ToDoListItem, self).__init__(**kwargs)
        self.press_event = None

    def refresh_view_attrs(self, rv, index, data):
        self.ids.edit_button.opacity = 0
        self.ids.edit_button.disabled = True
        self.ids.delete_button.opacity = 0
        self.ids.delete_button.disabled = True
        # Ensure checkbox state is set according to the data
        self.ids.checkbox.active = data.get('is_done', False)
        return super(ToDoListItem, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Cancel showing buttons on other items
            self.hide_buttons_other_items()
            # Schedule showing the buttons after 1 second
            self.press_event = Clock.schedule_once(lambda dt: self.show_buttons(), 0.5)
        return super(ToDoListItem, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.press_event:
            # If touch is released before 1 second, cancel the scheduled event
            Clock.unschedule(self.press_event)
            self.press_event = None
        return super(ToDoListItem, self).on_touch_up(touch)

    def show_buttons(self, *args):
        # Show the buttons for this item
        self.ids.edit_button.opacity = 1
        self.ids.edit_button.disabled = False
        self.ids.delete_button.opacity = 1
        self.ids.delete_button.disabled = False

    def hide_buttons(self):
        # Hide the buttons
        self.ids.edit_button.opacity = 0
        self.ids.edit_button.disabled = True
        self.ids.delete_button.opacity = 0
        self.ids.delete_button.disabled = True

    def hide_buttons_other_items(self):
        current_screen = App.get_running_app().root.current_screen
        if hasattr(current_screen, 'ids') and 'rv' in current_screen.ids:
            for item in current_screen.ids.rv.children[0].children:
                if item != self:
                    item.hide_buttons()

    def on_checkbox_change(self, checkbox, value):
        for item in App.get_running_app().root.get_screen('main').ids.rv.data:
            task_uuid = item['id']
            if task_uuid == self.id:
                item['is_done'] = value
                TaskStorageHandler._set_task_state(task_uuid, bool(value))

    def on_data(self, *args):
        # Explicitly reset the checkbox state based on the item's data
        self.ids.checkbox.active = self.is_done


class MainToDoList(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

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

        TaskStorageHandler._add_task(str(mqtt_client.config.client_id), text)

        data = TaskStorageHandler._read_data(True)
        mqtt_client.publish_message(data, True)

    def delete_item(self, task_uuid):

        TaskStorageHandler._delete_task(task_uuid)

        self.ids.rv.data = [item for item in self.ids.rv.data if item['id'] != task_uuid]

        data = TaskStorageHandler._read_data()
        tasks = data["tasks"]
        self.load_tasks_in_local_list(tasks)

        data = TaskStorageHandler._read_data(True)
        mqtt_client.publish_message(data, True)

    def edit_item(self, item_widget):
        # Trigger editing using the item's widget but reference by ID
        self.selected_item_id = item_widget.id  # Store the selected item's ID
        self.ids.global_edit_text.text = item_widget.text
        self.ids.global_edit_text.disabled = False
        self.ids.global_edit_text.opacity = 1
        self.ids.global_edit_text.focus = True
        # 1. Das Item mit der UUID finden und in der .json auch umbenennen.
        # 2. Liste neu laden und Publicchhhen

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


class LoginScreen(Screen):

    def connect(self, username_input, password_input, topic_input):
        mqtt_client.client.connect(config.broker_adress, config.port)

        username = username_input
        password = password_input
        topic = topic_input


class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class ToDoApp(MDApp):

    def build(self):
        Builder.load_file('resources/layout.kv')
        self.icon = 'resources/app_icon.png'
        sm = ScreenManager()

        todoscreen = MainToDoList(name='main')
        loginscreen = LoginScreen(name='login')

        sm.add_widget(todoscreen)
        sm.add_widget(loginscreen)
        # Lese alles aus tasks.json
        # For element in tasks:

        data = TaskStorageHandler._read_data()
        tasks = data["tasks"]

        todoscreen.load_tasks_in_local_list(tasks)
        return sm

    def change_color(self, instance):
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            for i in range(3):  # Je nach dem wie viele Icons
                if f"nav_icon{i + 1}" == current_id:
                    self.root.ids[f"nav_icon{i + 1}"].text_color = 1, 0, 0, 1
                else:
                    self.root.ids[f"nav_icon{i + 1}"].text_color = 0, 0, 0, 1


if __name__ == '__main__':
    ToDoApp().run()
