from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock


Builder.load_file('resources/layout.kv')

class ToDoListItem(BoxLayout):
    text = StringProperty('')
    is_done = BooleanProperty(False)  # Keeps track of whether the task is done

    def __init__(self, **kwargs):
        super(ToDoListItem, self).__init__(**kwargs)
        self.press_event = None

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
        # Hide buttons on all items except this one
        for item in App.get_running_app().root.ids.rv.children[0].children:
            if item != self:
                item.hide_buttons()

    def on_checkbox_active(self, checkbox, value):
        # You can handle task completion logic here
        self.is_done = value
        print(f"Task '{self.text}' completion status: {self.is_done}")

    def checkbox_trigger(self):
        # We'll toggle the checkbox's 'active' property
        self.ids.checkbox.active = not self.ids.checkbox.active


class MainToDoList(BoxLayout):
    def add_item(self):
        # Adds a new item with a placeholder text
        new_task_text = f'New Task {len(self.ids.rv.data) + 1}'
        self.ids.rv.data.append({'text': new_task_text})

    def delete_item(self, item_widget):
        # Deletes an item based on its text
        self.ids.rv.data = [item for item in self.ids.rv.data if item['text'] != item_widget.text]
        self.ids.rv.refresh_from_data()

    def edit_item(self, item_widget):
        self.selected_item = item_widget
        self.ids.global_edit_text.text = item_widget.text
        print('self.ids.global_edit_text.text  ->  '+str(self.ids.global_edit_text.text))
        self.ids.global_edit_text.disabled = False
        self.ids.global_edit_text.opacity = 1
        self.ids.global_edit_text.focus = True

    def apply_global_edit(self):
        if self.selected_item:
            new_text = self.ids.global_edit_text.text
            # Update the selected item text and refresh the RecycleView
            print('self.selected_item.text  ->  '+str(self.selected_item.text))
            for item in self.ids.rv.data:
                if item['text'] == self.selected_item.text:
                    item['text'] = new_text
                    print("item['text']  -> "+str(item['text']))
                    break
            self.ids.rv.refresh_from_data()
            # Checke input der safe.json -> Wenn status = checked dann checke und wenn nicht dann unchecke
            # For element in safe.json:

            # Clear and hide the global TextInput
            self.ids.global_edit_text.text = ''
            self.ids.global_edit_text.opacity = 0
            self.ids.global_edit_text.disabled = True
            self.selected_item = None

class ToDoApp(App):
    def build(self):
        return MainToDoList()

if __name__ == '__main__':
    ToDoApp().run()
