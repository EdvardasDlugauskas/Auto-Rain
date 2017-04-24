import win32timezone
import encodings.idna  # required for PyInstaller

from kivy.app import App
from kivy.properties import StringProperty, ListProperty

from mainutils import *
from widgets import ListEntry, MainScreenManager


class RainApp(App):
    IMG_SAVE_PATH = StringProperty(
        ".")  # "C:\\Users\\Family\\Documents\\Rainmeter\\Skins\\Dektos by Tibneo\\Dock\\Left\\Icons"
    APP_PATH = StringProperty(".")  # 'C:\\Users\\Family\\Desktop\\Root\\Games' # Insert folder file
    INI_PATH = StringProperty(".")  # "C:\\Users\\Family\\Documents\\Rainmeter\\Skins\\Dektos by Tibneo\\Dock\\Left"

    main = ObjectProperty(None)
    icon = ListProperty([])

    def __init__(self):
        super().__init__()

    def build(self):
        self.set_paths()
        self.main = MainScreenManager()
        self.populate_main()

        return self.main

    def rebuild_main(self):
        """
        After saving new icons, the list needs to be reloaded.
        
        """
        self.main.current_screen.ids.entry_list.clear_widgets()
        self.populate_main()

    def populate_main(self):
        loop = asyncio.get_event_loop()
        icons = loop.run_until_complete(get_icon_objs(self))
        icons = sort_by_ini(icons, path.join(self.INI_PATH, "Left Dock.ini"))

        for i, icon in enumerate(icons, start=1):
            # Reverse order for the right index
            new = ListEntry(icon, len(icons) - i)
            self.main.current_screen.ids.entry_list.add_widget(new)

    def reload_images(self):
        for entry in self.main.current_screen.ids.entry_list.children:
            entry.set_image()

    def build_config(self, config):
        config.setdefaults('paths', {
            'IMG_SAVE_PATH': '.',
            'APP_PATH': '.',
            'INI_PATH': '.'
        })

    def set_paths(self):
        config = self.config
        self.APP_PATH = config.get("paths", "APP_PATH")
        self.INI_PATH = config.get("paths", "INI_PATH")
        self.IMG_SAVE_PATH = config.get("paths", "IMG_SAVE_PATH")

    def select_path(self, target: str):
        popup = Popup(size_hint=(.9, .9), title="Select path")

        browser = FileBrowser(select_string='Save', dirselect=True,
                              show_hidden=False, filters=["!.sys"])

        default_path = getattr(self, target)
        if path.exists(default_path):
            browser.path = default_path

        def success(instance):
            setattr(self, target, browser_selection(browser))
            if target in ("APP_PATH",):  # Needs rebuild
                self.main.current_screen.needs_rebuild = True
            popup.dismiss()

        browser.bind(on_success=success,
                     on_canceled=popup.dismiss)

        popup.add_widget(browser)
        popup.open()

    def save_rainmeter_config(self):
        save_rainmeter_configuration(self)

    def save_path_config(self):
        config = self.config
        config.set("paths", "APP_PATH", self.APP_PATH)
        config.set("paths", "INI_PATH", self.INI_PATH)
        config.set("paths", "IMG_SAVE_PATH", self.IMG_SAVE_PATH)
        config.write()


if __name__ == '__main__':
    try:
        RainApp().run()
    except Exception as e:
        import traceback

        print("An exception occurred:", traceback.format_exc())
        with open("errorlog.txt", "w") as errorfile:
            errorfile.write(traceback.format_exc())
        raise


"""
# Set widget colour
canvas.before:
    Color:
        rgba: 1, 0, 1, 1
    Rectangle:
        pos: self.pos
        size: self.size
"""
