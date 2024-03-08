from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from logic.storage.TaskStorageHandler import TaskStorageHandler
from logic.mqtt.MqttHandler import MqttHandler
from logic.mqtt.MqttConfig import MqttConfig
# Screens importieren
from ui.screens.MainScreen import MainToDoList
from ui.screens.SettingScreen import LoginScreen

# Die zwei Statements müssen drin bleiben, das sonst
from ui.components.TodolistItem import ToDoListItem
from ui.components.NavigationBar import NavBar




class ToDoApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = MqttConfig.load_from_resource()
        self.mqtt_client = MqttHandler(self.config)

    def build(self):
        Builder.load_file('resources/layout.kv')
        self.icon = 'resources/app_icon.png'
        sm = ScreenManager()

        #Generiere UUID und aktualisiere sie
        todoscreen = MainToDoList(name='main', mqtt_client=self.mqtt_client)
        loginscreen = LoginScreen(name='login', mqtt_client=self.mqtt_client)

        sm.add_widget(todoscreen)
        sm.add_widget(loginscreen)

        data = TaskStorageHandler._read_data()
        tasks = data["tasks"]
        print('Hallo1111')
        todoscreen.load_tasks_in_local_list(tasks)
        return sm


if __name__ == '__main__':
    ToDoApp().run()
