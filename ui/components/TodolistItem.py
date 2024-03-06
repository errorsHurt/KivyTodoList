import json
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.properties import ObjectProperty

from logic.mqtt.MqttConfig import MqttConfig
from logic.mqtt.MqttHandler import MqttHandler
from logic.storage.TaskStorageHandler import TaskStorageHandler


class ToDoListItem(BoxLayout):
    checkbox = ObjectProperty(None)
    uuid = StringProperty('')
    text = StringProperty('')
    is_done = BooleanProperty(False)  # Keeps track of whether the task is done

    def __init__(self, **kwargs):
        super(ToDoListItem, self).__init__(**kwargs)

        self.config = MqttConfig.load_from_resource()
        self.mqtt_client = MqttHandler(self.config)

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

    def sync_items(self):
        msg = self.mqtt_client.lissen()
        print(msg)
        if msg:
            try:
                msg = msg.replace("'", "\"").replace("True", "true").replace("False", "false")
                data = json.loads(msg)
                TaskStorageHandler._write_data(data)
                #self.load_tasks_in_local_list(data["tasks"])

            except json.JSONDecodeError as e:
                print("Fehler:", e)

    def on_checkbox_change(self, checkbox, value):
        msg = self.mqtt_client.lissen()
        for item in App.get_running_app().root.get_screen('main').ids.rv.data:
            task_uuid = item['id']
            if task_uuid == self.id:
                item['is_done'] = value

                self.sync_items()
                TaskStorageHandler._set_task_state(task_uuid, bool(value))
                data = TaskStorageHandler._read_data()
                self.mqtt_client.publish_message(str(data), True)

    def on_data(self, *args):
        # Explicitly reset the checkbox state based on the item's data
        self.ids.checkbox.active = self.is_done
