import threading
from copy import copy
from os import path

from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.garden.filebrowser import FileBrowser, get_home_directory
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from files_get import get_icon_objs, CONST_INFO, TEMPLATE, INI_PATH
from icon_get import url_to_bytes, save_full_icon


class MainWidget(GridLayout):
    def move_entry_up(self, index):
        children = self.ids.entry_list.children
        if index > 0:
            children[index], children[index - 1] = children[index - 1], children[index]
            children[index].index, children[index - 1].index = children[index - 1].index, children[index].index

    def move_entry_down(self, index):
        children = self.ids.entry_list.children
        if index < len(children) - 1:
            children[index], children[index + 1] = children[index + 1], children[index]
            children[index].index, children[index + 1].index = children[index + 1].index, children[index].index


# TODO: add progress bar?
class OptionsPopup(Popup):
    img = ObjectProperty(None)

    # Make options popup img change together/without the entry img
    # Copy Icon object in entry, mingle with it, then save/discard it
    def __init__(self, entry, **kwargs):
        super().__init__(**kwargs)
        self.entry = entry
        self.icon = copy(entry.icon)

        self.img = AsyncImage(allow_stretch=False)
        self.set_image()

        self.ids.popup_layout.add_widget(self.img)

    def next_image(self):
        self.icon.get_next_icon_url()
        self.img.texture = CoreImage(self.icon.current_icon_bytes(), ext="png").texture

    def previous_image(self):
        self.icon.get_previous_icon_url()
        self.img.texture = CoreImage(self.icon.current_icon_bytes(), ext="png").texture

    def set_image(self):
        self.img.texture = CoreImage(self.icon.current_icon_bytes(), ext="png").texture

    def save(self):
        self.entry.icon = self.icon
        self.entry.img.texture = self.img.texture
        self.dismiss()


class ListEntry(ButtonBehavior, BoxLayout):
    img = ObjectProperty(None)
    icon = ObjectProperty(None)

    def __init__(self, icon, index, **kwargs):
        super().__init__(**kwargs)

        self.index = index
        self.icon = icon
        self.ids.icon_info.text = icon.name

        self.img = AsyncImage(height=self.height, allow_stretch=True,
                              size_hint=(.1, 1))

        self.add_widget(self.img, index=len(self.children) - 1)

    def set_image(self):
        # Crop img if it exists already
        if self.icon.icon_on_disk:
            core_img = CoreImage(self.icon.bytes_on_disk, ext="png")

        else:
            core_img = core_img_from_url(self.icon.get_next_icon_url())

        self.img.texture = core_img.texture

    def show_options_popup(self):
        popup = OptionsPopup(self)
        popup.open()


class RainApp(App):
    main = ObjectProperty(None)
    select_popup = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.icons = None

    def build(self):
        self.icons = get_icon_objs()
        self.main = MainWidget()
        for i, icon in enumerate(self.icons):
            new = ListEntry(icon, i)
            self.main.ids.entry_list.add_widget(new)

        for entry in self.main.ids.entry_list.children:
            entry.set_image()

        return self.main

    def rebuild_main(self):
        self.icons = get_icon_objs()
        self.main.ids.entry_list.clear_widgets()

        for i, icon in enumerate(self.icons):
            new = ListEntry(icon, i)
            self.main.ids.entry_list.add_widget(new)

        for entry in self.main.ids.entry_list.children:
            entry.set_image()

        return self.main

    def open_file_select(self, target: str):
        open_file_selection_popup(target)

    def save_config(self):
        write_thread = threading.Thread(target=self.write_info)
        write_thread.start()

        self.rebuild_main()

        write_thread.join()

        popup = Popup(size_hint=(.5, .5), title="Success!")
        popup.add_widget(Label(text="Saved successfully."))
        popup.open()

    def write_info(self):
        with open(path.join(INI_PATH, "Left Dock.ini"), "w") as ini_file:
            ini_file.write(CONST_INFO)
            for entry in reversed(self.main.ids.entry_list.children):
                ini_file.write(TEMPLATE.format(entry.icon.name, entry.icon.icon_path, entry.icon.file_path))
                save_full_icon(entry.icon.current_icon_bytes(), entry.icon.icon_path)


def open_file_selection_popup(target_name: str):
    popup = Popup(size_hint=(.9, .9), title="Select path")

    browser = FileBrowser(select_string='Save', dirselect=True, show_hidden=False)
    browser.bind(on_success=_fbrowser_success,
                 on_canceled=popup.dismiss)

    popup.add_widget(browser)
    popup.open()


def _fbrowser_success(instance: FileBrowser):
    if not instance.selection:
        selection = instance.path
    else:
        selection = instance.selection[0]  # since we aren't using multiselect

    selection = selection.replace("/", "\\")  # kivy bug workaround
    if selection.startswith("\\"):
        selection = get_home_directory().split("\\")[0] + selection

    return selection


def core_img_from_url(url):
    return CoreImage(url_to_bytes(url), ext="png")


if __name__ == '__main__':
    RainApp().run()

"""
# Set widget colour
canvas.before:
    Color:
        rgba: 1, 0, 1, 1
    Rectangle:
        pos: self.pos
        size: self.size


"""
