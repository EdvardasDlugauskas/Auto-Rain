from os import path, listdir

from icon_get import get_urls, url_to_bytes, crop_icon_back


class UrlBytes:
    def __init__(self, url, bytes):
        self.url = url
        self.bytes = bytes


class Icon:
    # TODO: use official Google API
    GOOGLE_URL_TEMPLATE = "https://www.google.com/search?q={}+icon+filetype:png&tbm=isch&source=lnt&tbs=iar:s"
    index = -1

    def __init__(self, name: str,
                 image_save_path: str):

        self.name = name
        self.image_save_path = image_save_path

        self.url_bytes = []
        self.icon_path = self.bytes_on_disk = None
        self.set_icon_path()  # sets icon_path and bytes_on_disk

    @property
    def icon_on_disk(self):
        if self.bytes_on_disk:
            return True
        else:
            return False


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

        return self.url_bytes[self.index].url

    def get_next_icon_url(self):
        self.index += 1

        return self.get_current_icon_url()

    def get_previous_icon_url(self):
        self.index -= 1

        return self.get_current_icon_url()
