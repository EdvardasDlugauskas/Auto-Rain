from typing import List
from os import path, listdir
from collections import namedtuple
from io import BytesIO

from PIL import ImageEnhance, Image, ImageOps, ImageDraw
from bs4 import BeautifulSoup
from requests import get

from icon_get import get_urls, url_to_bytes


class UrlBytes:
    def __init__(self, url, bytes):
        self.url = url
        self.bytes = bytes


class Icon:
    GOOGLE_URL_TEMPLATE = "https://www.google.com/search?q={}+icon+filetype:png&tbm=isch&source=lnt&tbs=iar:s"
    IMG_SAVE_PATH = "."  # "C:\\Users\\Family\\Documents\\Rainmeter\\Skins\\Dektos by Tibneo\\Dock\\Left\\Icons" # Where are the icons saved?

    index = -1

    def __init__(self, name: str,
                 file_path: str = None,
                 icon_path: str = None,
                 urls: List[str] = None):

        self.name = name
        self.file_path = file_path
        self.icon_path = icon_path

        self.url_bytes = []
        self.check_urls()

        self.icon_on_disk = None
        self.set_icon_path()  # sets icon_on_disk as well

    def set_icon_path(self):
        icon_name = self.name + " icon.png"
        icon_full_path = path.join(self.IMG_SAVE_PATH, icon_name)

        self.icon_on_disk = True if icon_name in listdir(self.IMG_SAVE_PATH) else False
        self.icon_path = icon_full_path

    def current_icon_bytes(self):
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

        return self.url_bytes[self.index].url

    def get_next_icon_url(self):
        self.index += 1

        return self.get_current_icon_url()

    def get_previous_icon_url(self):
        self.index -= 1

        return self.get_current_icon_url()
