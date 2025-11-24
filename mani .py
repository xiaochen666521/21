from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivy.core.window import Window
from kivy.utils import platform
import json
import os

if platform != 'android':
    Window.size = (360, 640)

class TaskItem(OneLineAvatarIconListItem):
    def __init__(self, text, is_completed, delete_callback, toggle_callback, **kwargs):
        super().__init__(text=text, **kwargs)
        self.delete_callback = delete_callback
        self.toggle_callback = toggle_callback
        self.is_completed = is_completed
        self.icon_left = IconLeftWidget(icon="checkbox-marked-circle-outline" if is_completed else "checkbox-blank-circle-outline")
        self.icon_left.bind(on_release=self.on_checkbox_click)
        self.add_widget(self.icon_left)
        self.icon_right = IconRightWidget(icon="trash-can-outline", theme_text_color="Error")
        self.icon_right.bind(on_release=lambda x: delete_callback(self))
        self.add_widget(self.icon_right)

    def on_checkbox_click(self, instance):
        self.is_completed = not self.is_completed
        self.icon_left.icon = "checkbox-marked-circle-outline" if self.is_completed else "checkbox-blank-circle-outline"
        self.toggle_callback()

class ZenithApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.data_file = "tasks.json"
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title="每日规划")
        toolbar.elevation = 4
        layout.add_widget(toolbar)
        scroll = MDScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        input_box = MDBoxLayout(size_hint_y=None, height="60dp", padding="10dp", spacing="10dp")
        self.text_input = MDTextField(hint_text="添加新任务...", mode="rectangle", size_hint_x=0.8)
        add_btn = MDIconButton(icon="plus-circle", theme_text_color="Custom", text_color=self.theme_cls.primary_color, on_release=self.add_task)
        input_box.add_widget(self.text_input)
        input_box.add_widget(add_btn)
        layout.add_widget(input_box)
        screen.add_widget(layout)
        return screen

    def on_start(self):
        self.load_data()

    def add_task(self, instance):
        if self.text_input.text:
            self.create_item(self.text_input.text, False)
            self.text_input.text = ""
            self.save_data()

    def create_item(self, text, is_completed):
        item = TaskItem(text=text, is_completed=is_completed, delete_callback=self.delete_item, toggle_callback=self.save_data)
        self.list_view.add_widget(item)

    def delete_item(self, item_widget):
        self.list_view.remove_widget(item_widget)
        self.save_data()

    def save_data(self):
        tasks = [{"text": w.text, "completed": w.is_completed} for w in reversed(self.list_view.children)]
        with open(self.data_file, "w") as f:
            json.dump(tasks, f)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    for t in json.load(f): self.create_item(t['text'], t['completed'])
            except: pass

if __name__ == "__main__":
    ZenithApp().run()