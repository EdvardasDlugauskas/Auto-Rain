import asyncio
import re
from os import path, scandir
from typing import List

from kivy.uix.label import Label
from kivy.uix.popup import Popup

from const_info import CONST_INFO, TEMPLATE, VALID_EXTENSIONS
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
        app.reload_images()
    except Exception as e:
        title = "Error!"
        text = str(e)

    popup = Popup(size_hint=(.45, .30), title=title)
    popup.add_widget(Label(text=text, font_size=15))
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
            ini_file.write(TEMPLATE.format(icon.name, icon.icon_path, icon.app_path))
            save_full_icon(icon.current_icon_bytes(), icon.icon_path)
            icon.load_icon_from_disk()


def save_path_configuration(app):
    config = app.config
    config.set("paths", "APP_PATH", app.APP_PATH)
    config.set("paths", "INI_PATH", app.INI_PATH)
    config.set("paths", "IMG_SAVE_PATH", app.IMG_SAVE_PATH)
    config.write()

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
            valid_files.append(Icon(name=name, image_save_path=app.IMG_SAVE_PATH, app_path=program.path))

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


def sort_by_ini(icons: List[Icon], ini_path: str = None, ini_str: str = None) -> List[Icon]:
    try:
        if ini_path is ini_str is None:
            raise ValueError("No .ini path or string provided.")

        text = ""
        if ini_path:
            with open(ini_path) as file:
                text = file.read()
        elif ini_str:
            text = ini_str

        text = text.split("APPLICATION")[1]
        pattern = "\[(.*?)\]"
        sort_list = re.findall(pattern, text)

        return sorted(icons, key=lambda x: sort_list.index(x.name) if x.name in sort_list else -1)

    except Exception as e:
        print("Sorting by ini exception: ")
        print(e)
        return icons
