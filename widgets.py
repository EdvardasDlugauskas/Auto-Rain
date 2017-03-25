from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager

from icon_get import core_img_from_url
from mainutils import OptionsPopup


class MainScreen(Screen):
    """
    on_scroll_change and on_slider_change bind the slider and scrollview together.
    """

    @staticmethod
    def scroll_change(scrollview, slider_instance):
        scrollview.scroll_y = slider_instance.value_normalized

    @staticmethod
    def slider_change(slider, scrlview_instance):
        if scrlview_instance.scroll_y >= 0:
            # this to avoid 'maximum recursion depth exceeded' error, according to docs
            slider.value = scrlview_instance.scroll_y


class SettingsScreen(Screen):
    pass


# TODO: this bug again?
class MainScreenManager(ScreenManager):
    def move_entry_down(self, index: int):
        children = self.current_screen.ids.entry_list.children
        if index > 0:
            children[index], children[index - 1] = children[index - 1], children[index]
            children[index].index, children[index - 1].index = children[index - 1].index, children[index].index

    def move_entry_up(self, index: int):
        children = self.current_screen.ids.entry_list.children
        if index < len(children) - 1:
            children[index], children[index + 1] = children[index + 1], children[index]
            children[index].index, children[index + 1].index = children[index + 1].index, children[index].index


class ListEntry(ButtonBehavior, BoxLayout):
    img = ObjectProperty(None)
    icon = ObjectProperty(None)

    def __init__(self, icon, index: int, **kwargs):
        super().__init__(**kwargs)

        self.index = index
        self.icon = icon
        self.ids.icon_info.text = icon.name

        self.img = AsyncImage(height=self.height, allow_stretch=True,
                              size=(56, 56), size_hint=(None, None))

        self.add_widget(self.img, index=len(self.children) - 1)

        self.set_image()

    def set_image(self):
        # Crop img if it exists already
        if self.icon.icon_on_disk:
            self.icon.bytes_on_disk.seek(0)
            core_img = CoreImage(self.icon.bytes_on_disk, ext="png")

        else:
            core_img = core_img_from_url(self.icon.get_next_icon_url())

        self.img.texture = core_img.texture

    def open_entry_options_popup(self):
        popup = OptionsPopup(self, auto_dismiss=False)
        popup.open()
