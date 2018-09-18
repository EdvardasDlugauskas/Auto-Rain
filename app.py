import os

import win32timezone
import encodings.idna  # required for PyInstaller

from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from mainutils import *
from widgets import ListEntry, MainScreenManager, WrappedLabel


class RainApp(App):
	"""
	Main AutoRain app.
	"""
	IMG_SAVE_PATH = StringProperty(".")
	APP_PATH = StringProperty(".")
	INI_PATH = StringProperty(".")

	main = ObjectProperty(None)

	# For initialization errors
	init_errors = ""

	def __init__(self):
		super().__init__()

	def build(self):
		self.set_paths()
		self.main = MainScreenManager()
		self.populate_main()

		if self.init_errors:
			Popup(size_hint=(.7, .7), title="Errors found",
			      content=WrappedLabel(text=self.init_errors)).open()

		return self.main

	def rebuild_main(self):
		"""
		After saving new icons, the list needs to be reloaded.
		
		"""
		self.main.current_screen.ids.entry_list.clear_widgets()
		self.populate_main()

	def populate_main(self):
		"""
		Get the icons asynchronously, in-place.
		"""
		loop = asyncio.get_event_loop()
		icons = loop.run_until_complete(get_icon_objs(self))
		icons = sort_by_ini(icons, path.join(self.INI_PATH, "Dock.ini"))

		for icon in icons:
			# Reverse order for the right index
			new = ListEntry(icon)
			self.main.current_screen.ids.entry_list.add_widget(new)

	def reload_images(self):
		"""
		Reload the images of icon objects.
		"""
		for entry in self.main.current_screen.ids.entry_list.children:
			entry.set_image()

	def build_config(self, config):
		"""
		Builds a config if there isn't one.
		"""
		config.setdefaults('paths', {
			'IMG_SAVE_PATH': '.',
			'APP_PATH': '.',
			'INI_PATH': '.'
		})

	def set_paths(self):
		"""
		Reads the paths from the rain.ini file and uses them.
		Checks that paths exist and sets to default if they don't.
		"""
		default_path = os.path.expanduser("~")
		config = self.config
		self.APP_PATH = config.get("paths", "APP_PATH")
		if not os.path.exists(self.APP_PATH):
			self.init_errors += f"Could not find path for apps/games:" \
			                    f" '{self.APP_PATH}'. Setting to default for now.\n\n"
			self.APP_PATH = default_path

		self.INI_PATH = config.get("paths", "INI_PATH")
		if not os.path.exists(self.INI_PATH):
			self.init_errors += f"Could not find path for .ini file:" \
			                    f" '{self.INI_PATH}'. Setting to default for now.\n\n"
			self.INI_PATH = default_path

		self.IMG_SAVE_PATH = config.get("paths", "IMG_SAVE_PATH")
		if not os.path.exists(self.IMG_SAVE_PATH):
			self.init_errors += f"Could not find path for storing icons:" \
			                    f" '{self.IMG_SAVE_PATH}'. Setting to default for now.\n\n"
			self.IMG_SAVE_PATH = default_path

	def select_path(self, target: str):
		"""
		Opens a popup for selecting a path. Implicitly replaces the internal value
		called `target` to the path returned by the selection popup.
		:param target: string for the target internal variable to set
		"""
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

		browser.bind(on_success=success, on_canceled=popup.dismiss)

		popup.add_widget(browser)
		popup.open()


if __name__ == '__main__':
	try:
		RainApp().run()
	except Exception as e:
		import traceback

		# print("An exception occurred:", traceback.format_exc())
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
