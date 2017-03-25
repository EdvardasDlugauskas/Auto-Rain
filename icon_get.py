from io import BytesIO

from PIL import ImageEnhance, Image, ImageOps, ImageDraw
from bs4 import BeautifulSoup
from kivy.core.image import Image as CoreImage
from requests import get

ICON_SIZE = 48, 48
BIG_MASK_SIZE = 256, 256  # Used for anti-aliasing

# Filetype is always PNG
GOOGLE_URL_TEMPLATE = "https://www.google.com/search?q={}+icon+filetype:png&tbm=isch&source=lnt&tbs=iar:s"

OVERWRITE_ICONS = False


def core_img_from_url(url):
    return CoreImage(url_to_bytes(url), ext="png")


def file_to_bytes(file_path):
    with open(file_path) as f:
        byte_array = BytesIO(f.read())

    return byte_array


def crop_icon_back(icon_path):
    img = Image.open(icon_path)
    cropped = img.crop((0, 0, ICON_SIZE[0], ICON_SIZE[0]))

    byte_array = BytesIO()  # empty bytes
    cropped.save(byte_array, format="png")
    byte_array.seek(0)  # because PIL seeks to the end and kivy reads again

    return byte_array


def url_to_bytes(url):
    img_response = get(url, stream=True)
    return BytesIO(img_response.content)


def get_image(search_term):
    try:
        img_element = get_urls(search_term)[0]
    except IndexError:
        raise Exception("Could not find img: " + search_term)

    byte_array = url_to_bytes(img_element)

    return Image.open(byte_array)


def get_urls(search_term):
    parsed_response = BeautifulSoup(get(GOOGLE_URL_TEMPLATE.format(search_term)).text, "html.parser")
    return [x['src'] for x in parsed_response.find_all("img")]


def save_full_icon(image_bytes, save_path):
    image = Image.open(image_bytes)

    image.thumbnail(ICON_SIZE, Image.ANTIALIAS)
    w, h = ICON_SIZE

    new_image = Image.new("RGBA", (w * 3, h))
    img_two = ImageEnhance.Sharpness(image.convert("RGB"))
    img_three = ImageEnhance.Brightness(image.convert("RGB"))

    new_image.paste(make_alpha_icon(image), (0, 0))
    new_image.paste(make_alpha_icon(img_two.enhance(2)), (w, 0))
    new_image.paste(make_alpha_icon(img_three.enhance(1.5)), (w * 2, 0))

    new_image.save(save_path)


def make_alpha_icon(image):
    mask = Image.new('L', BIG_MASK_SIZE, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + BIG_MASK_SIZE, fill=255)
    mask = mask.resize(ICON_SIZE, Image.ANTIALIAS)

    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    return output
