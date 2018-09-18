from io import BytesIO

from PIL import ImageEnhance, Image, ImageOps, ImageDraw, ImageChops
from bs4 import BeautifulSoup
from kivy.core.image import Image as CoreImage
from requests import get

from const_info import ICON_SIZE

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


def get_urls(search_term):
    parsed_response = BeautifulSoup(get(GOOGLE_URL_TEMPLATE.format(search_term)).text, "html.parser")
    return [x['src'] for x in parsed_response.find_all("img") if x['src'].startswith("http")]


def save_full_icon(image_bytes, save_path):
    image = Image.open(image_bytes)
    # image.convert("RGBA")

    # draw = ImageDraw.Draw(image)
    # draw.rectangle(xy=(0, 0, image.width-1, image.height-1), outline=6)

    # Absolutely needed for some reason, do not remove
    # del draw

    image.thumbnail(ICON_SIZE, 0)  # Image.ANTIALIAS)
    w, h = ICON_SIZE

    # The three thumbnail images
    new_image = Image.new("RGBA", (w * 3, h))
    img_two = ImageEnhance.Sharpness(image.convert("RGB"))
    img_three = ImageEnhance.Brightness(image.convert("RGB"))

    # Paste them in order
    new_image.paste(image, (0, 0))
    new_image.paste(img_two.enhance(2), (w, 0))
    new_image.paste(img_three.enhance(1.5), (w * 2, 0))

    """ # For altered shape use
    new_image.paste(make_into_shape(image), (0, 0))
    new_image.paste(make_into_shape(img_two.enhance(2)), (w, 0))
    new_image.paste(make_into_shape(img_three.enhance(1.5)), (w * 2, 0))

    """



    new_image.save(save_path)


def make_into_shape(image):
    mask = Image.new('L', BIG_MASK_SIZE, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + BIG_MASK_SIZE, fill=255)
    mask = mask.resize(ICON_SIZE, Image.ANTIALIAS)

    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    return output


def make_white_transparent(img: Image):
    """
    Makes the white (background) transparent. Inplace.
    :param img: Image object to change inplace
    :return: None
    """
    # Access to pixel data
    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)


def trim(im, border=(255, 255, 255, 255)):
    """
    Trims whitespace around an image.
    :param im:
    :param border:
    :return:
    """
    bg = Image.new("RGBA", im.size, "white")
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        # found no content
        raise ValueError("Cannot trim - image was empty.")
