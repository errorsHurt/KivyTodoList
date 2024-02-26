from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout

Window.size = (310, 580)


class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class BottomNavbar(MDApp):

    def build(self):
        return Builder.load_file("bottomnavbar.kv")
        # return Builder.load_string(kv)

    def change_color(self, instance):
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            # print(current_id)
            for i in range(3):  # Je nach dem wie viele Icons
                if f"nav_icon{i + 1}" == current_id:
                    self.root.ids[f"nav_icon{i + 1}"].text_color = 1, 0, 0, 1
                else:
                    self.root.ids[f"nav_icon{i + 1}"].text_color = 0, 0, 0, 1


if __name__ == "__main__":
    BottomNavbar().run()