from os import path, listdir

from kivy.core.image import Image as CoreImage

from icon_get import get_urls, url_to_bytes, crop_icon_back, core_img_from_url


class UrlBytes:
	def __init__(self, url, bytes):
		self.url = url
		self.bytes = bytes


class IconManager:
	"""
	Manages the icons for an app.
	"""
	# TODO: use official Google API
	GOOGLE_URL_TEMPLATE = "https://www.google.com/search?q={}+icon+filetype:png&tbm=isch&source=lnt&tbs=iar:s"

	def __init__(self, name: str,
	             image_save_path: str,
	             app_path: str):

		self.name = name
		self.image_save_path = image_save_path
		self.app_path = app_path
		self.index = -1

		self.url_bytes = []
		self.icon_path = self.bytes_on_disk = None
		self.set_icon_path()  # sets icon_path and bytes_on_disk

	@property
	def core_image(self):
		if self.icon_on_disk:
			self.bytes_on_disk.seek(0)
			return CoreImage(self.bytes_on_disk, ext="png")

		else:
			return core_img_from_url(self.get_next_icon_url())

	@property
	def icon_on_disk(self):
		return bool(self.bytes_on_disk)

	def set_icon_path(self):
		icon_name = self.name + " icon.png"
		self.icon_path = path.join(path.abspath(self.image_save_path), icon_name)

		if icon_name in listdir(self.image_save_path):
			self.load_icon_from_disk()

	def load_icon_from_disk(self):
		self.bytes_on_disk = crop_icon_back(self.icon_path)

	def current_icon_bytes(self):
		if self.index == -1 and self.bytes_on_disk:
			self.bytes_on_disk.seek(0)
			return self.bytes_on_disk

		current_urlbytes = self.url_bytes[self.index]
		if current_urlbytes.bytes is None:
			current_urlbytes.bytes = url_to_bytes(current_urlbytes.url)

		current_urlbytes.bytes.seek(0)
		return current_urlbytes.bytes

	def check_urls(self):
		if not self.url_bytes:
			self.update_urls()

	def update_urls(self):
		urls = get_urls(self.name)
		for url in urls:
			self.url_bytes.append(UrlBytes(url, None))

		self.index = -1

	def get_current_icon_url(self):
		if self.index == len(self.url_bytes):
			self.index = 0
		elif self.index == -1:
			self.index = len(self.url_bytes) - 1

		if self.url_bytes:
			return self.url_bytes[self.index].url
		else:
			return None

	def get_next_icon_url(self):
		self.index += 1

		return self.get_current_icon_url()

	def get_previous_icon_url(self):
		self.index -= 1

		return self.get_current_icon_url()
