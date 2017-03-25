import asyncio
from copy import copy
from os import path, scandir

from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from files_get import CONST_INFO, TEMPLATE, VALID_EXTENSIONS
from icon import Icon
from icon_get import save_full_icon
from libs.garden.filebrowser import FileBrowser


def save_rainmeter_configuration(app):
    """
    Saves the .ini file and gives a notification popup on completion.
    :param app: RainApp - main application instance
    """
    title = "Success!"
    text = "Saved successfully."
    try:
        write_info(app)
        app.reload_main()
    except Exception as e:
        title = "Error!"
        text = str(e)
        raise

    popup = Popup(size_hint=(.45, .45), title=title)
    popup.add_widget(Label(text=text, font_size=20))
    popup.open()


def write_info(app):
    """
    Writes the .ini file and saves the icons.
    :param app: RainApp - main application instance
    :return: None
    """
    with open(path.join(app.INI_PATH, "Left Dock.ini"), "w") as ini_file:
        ini_file.write(CONST_INFO)
        for entry in reversed(app.main.current_screen.ids.entry_list.children):
            icon = entry.icon
            ini_file.write(TEMPLATE.format(icon.name, icon.icon_path, icon.image_save_path))
            save_full_icon(icon.current_icon_bytes(), icon.icon_path)
            icon.icon_on_disk = True


async def get_icon_objs(app):
    """
    Gets the icons for apps/games asynchronously
    :param app: RainApp instance
    :return:
    """

    directory = scandir(app.APP_PATH)
    accepted_programs = [x for x in directory if x.is_file()]

    valid_files = []
    for program in accepted_programs:
        name, extension = path.splitext(program.name)
        if extension in VALID_EXTENSIONS:
            valid_files.append(Icon(name=name, image_save_path=app.IMG_SAVE_PATH))

    # Async stuff
    loop = asyncio.get_event_loop()
    futures = [loop.run_in_executor(None, file.update_urls) for file in valid_files]

    for response in await asyncio.gather(*futures):
        pass

    return valid_files


def browser_selection(instance: FileBrowser):
    if not instance.selection:
        # If nothing is selected, choose current dir
        selection = instance.path
    else:
        selection = instance.selection[0]

    return selection


class OptionsPopup(Popup):
    img = ObjectProperty(None)

    def __init__(self, entry, **kwargs):
        super().__init__(**kwargs)
        self.entry = entry
        self.icon = copy(entry.icon)

        self.img = AsyncImage(allow_stretch=False)
        self.set_image()

        self.ids.popup_layout.add_widget(self.img, index=1)

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