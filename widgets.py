from functools import partial

from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.uix.behaviors import DragBehavior
from kivy.uix.scrollview import ScrollView

from icon_get import core_img_from_url

# y boundaries in range (0, 1)
LOWER_SCREEN_SCROLL_BOUNDARY = 0.10
UPPER_SCREEN_SCROLL_BOUNDARY = 0.85

Y_MAX_SCROLL_SPEED = 25
Y_MIN_SCROLL_SPEED = 3


class MyScroll(ScrollView):
	"""
	A scrollview with disabled scrolling by dragging the mouse.
	"""

	def on_touch_down(self, touch):
		# Block mouse dragging scrolls
		if touch.device == "mouse" and not touch.button.startswith("scroll"):
			self.do_scroll_y = False
			super().on_touch_down(touch)
			self.do_scroll_y = True
		else:
			# Don't block the mouse wheel scrolls
			super().on_touch_down(touch)


class MainScreen(Screen):
	""" TODO: remove this?
	on_scroll_change and on_slider_change bind the slider and scrollview together.
	"""

	def move_canvas_up(self, child):
		"""
		Draws some childs canvas over everything else.
		Useful when dragging an icon over other icons.
		"""
		self.canvas.remove(child.canvas)
		self.canvas.insert(len(self.canvas.get_group(None)), child.canvas)


class SettingsScreen(Screen):
	needs_rebuild = BooleanProperty(False)

	def rebuild_if_needed(self, app_instance):
		if self.needs_rebuild:
			app_instance.rebuild_main()
		self.needs_rebuild = False


class MainScreenManager(ScreenManager):
	pass


class ListEntry(DragBehavior, ButtonBehavior, BoxLayout):
	"""
	The main icon list entry. Is a grid with an icon and the name, can be clicked.
	"""
	img = ObjectProperty(None)
	icon = ObjectProperty(None)
	main_parent = ObjectProperty(None)
	is_scrolling = BooleanProperty(False)

	def __init__(self, icon, **kwargs):
		super().__init__(**kwargs)

		self.icon = icon
		self.ids.icon_info.text = icon.name
		self.main_parent = self.parent

		self.img = AsyncImage(height=self.height, allow_stretch=True, size=(56, 56), size_hint=(None, None))
		self.add_widget(self.img, index=len(self.children))
		self.set_image()

	def on_touch_down(self, touch):
		super().on_touch_down(touch)
		if not self.collide_point(*touch.pos):
			return

		if touch.grab_list and touch.grab_list[0]() is self:  # if this widget was grabbed
			self.main_parent = self.parent  # remember your parent

	def on_touch_move(self, touch):
		super().on_touch_move(touch)
		if not self.collide_point(*touch.pos):
			return
		# ?
		if touch.grab_list and touch.grab_current is self:  # if this widget was grabbed
			self.main_parent = self.parent  # remember your parent

			# make this widget be drawn on top
			self.parent.canvas.remove(self.canvas)
			self.parent.canvas.insert(len(self.parent.canvas.get_group(None)), self.canvas)

			x, y = touch.spos  # position in the 0-1 coordinate system
			if (y > 0.85 or y < 0.15) and not self.is_scrolling:
				self.scrolling = True
				Clock.schedule_once(partial(self.move_slider, touch), 0.05)

	def move_slider(self, touch, dt=None):
		if not touch.grab_list or not self.is_scrolling:
			self.is_scrolling = False
			return

		relative_touch_y = touch.spos[1]  # in range 0-1, the relative position on screen
		scrollview = self.main_parent.parent

		if relative_touch_y > UPPER_SCREEN_SCROLL_BOUNDARY:
			distance = ((relative_touch_y - UPPER_SCREEN_SCROLL_BOUNDARY) * 100) ** 2
			distance = Y_MAX_SCROLL_SPEED if distance > Y_MAX_SCROLL_SPEED \
				else Y_MIN_SCROLL_SPEED if distance < Y_MIN_SCROLL_SPEED \
				else distance  # in bounds
			scroll_distance = scrollview.convert_distance_to_scroll(0, distance)[1]

			if scrollview.scroll_y + scroll_distance <= 1:
				scrollview.scroll_y += scroll_distance
				self.center_y += distance
			else:
				distance = (1 - scrollview.scroll_y) * scrollview.height
				scrollview.scroll_y = 1
				self.center_y += distance

			Clock.schedule_once(partial(self.move_slider, touch), 0.03)

		elif relative_touch_y < LOWER_SCREEN_SCROLL_BOUNDARY:
			distance = ((LOWER_SCREEN_SCROLL_BOUNDARY - relative_touch_y) * 100) ** 2
			distance = Y_MAX_SCROLL_SPEED if distance > Y_MAX_SCROLL_SPEED \
				else Y_MIN_SCROLL_SPEED if distance < Y_MIN_SCROLL_SPEED \
				else distance  # in bounds
			scroll_distance = scrollview.convert_distance_to_scroll(0, distance)[1]

			if scrollview.scroll_y - scroll_distance >= 0:
				scrollview.scroll_y -= scroll_distance
				self.center_y -= distance
			else:
				distance = scrollview.scroll_y * scrollview.height
				scrollview.scroll_y = 0
				self.center_y -= distance

			Clock.schedule_once(partial(self.move_slider, touch), 0.03)

		else:
			self.is_scrolling = False

	def on_touch_up(self, touch):
		if self.collide_point(*touch.pos) and self._drag_touch:
			self.main_parent.remove_widget(self)
			new_index = self.get_new_index()
			self.main_parent.add_widget(self, index=new_index)

		super().on_touch_up(touch)

	def get_new_index(self):
		new_x, new_y = self.center_x, self.center_y
		children = list(self.main_parent.children)

		is_between = lambda x, x1, x2: x1 <= x <= x2 or x1 >= x >= x2

		# For edge cases
		if len(children) >= 2:
			if children[0].center_y > new_y:
				return 0
			elif children[-1].center_y < new_y:
				return len(children)

		for index, (child1, child2) in enumerate(zip(children[:-1], children[1:])):
			if is_between(new_y, child1.center_y, child2.center_y):
				return index + 1

	def set_image(self):
		'''
		# Crop img if it exists already
		if self.icon.icon_on_disk:
			self.icon.bytes_on_disk.seek(0)
			core_img = CoreImage(self.icon.bytes_on_disk, ext="png")

		else:
			core_img = core_img_from_url(self.icon.get_next_icon_url())
			'''

		self.img.texture = self.icon.core_image.texture

	def open_entry_options_popup(self):
		popup = ImageOptionsPopup(self)
		popup.open()


class ToggleImage(ToggleButtonBehavior, AsyncImage):
	"""
	The toggle image. Used when selecting a preferred icon from the grid.
	"""

	def __init__(self, main_parent, index, **kwargs):
		super().__init__(**kwargs)
		self.main_parent = main_parent
		self.index = index

	def on_touch_down(self, touch):
		# check for double taps first
		if self.collide_point(*touch.pos):
			if touch.is_double_tap:
				self.main_parent.save(self)

		super().on_touch_down(touch)

	def on_state(self, widget, value):
		if value == "down":
			# Darker
			self.color = [.8, .8, .8, .5]
		else:
			# Normal
			self.color = [1, 1, 1, 1]


class ImageOptionsPopup(Popup):
	"""
	Shows possible icons for an app/game. Lets user select one.
	"""
	def __init__(self, entry, **kwargs):
		super().__init__(**kwargs)
		self.entry = entry

		for i, icon_urlbytes in enumerate(entry.icon.url_bytes):
			aiw = ToggleImage(main_parent=self, index=i, source=icon_urlbytes.url)
			self.ids.image_grid.add_widget(aiw)

	def next_image(self):
		self.icon.get_next_icon_url()
		self.img.texture = CoreImage(self.icon.current_icon_bytes(), ext="png").texture

	def previous_image(self):
		self.icon.get_previous_icon_url()
		self.img.texture = CoreImage(self.icon.current_icon_bytes(), ext="png").texture

	def set_image(self):
		self.img.texture = CoreImage(self.icon.current_icon_bytes(), ext="png").texture

	def save(self, selection):
		self.entry.icon.index = selection.index
		self.entry.img.texture = selection.texture
		self.dismiss()


class WrappedLabel(ScrollView):
	""" A label with wrapped text and scrolling if needed."""
	text = StringProperty()

	def __init__(self, text, **kwargs):
		super().__init__(**kwargs)
		self.text = text
