from io import BytesIO
from os import path, listdir

from PIL import ImageEnhance, Image, ImageOps, ImageDraw
from bs4 import BeautifulSoup
from requests import get

ICON_SIZE = 64, 64
#GOOGLE_URL_TEMPLATE = "https://www.google.com/search?q={}+icon+filetype:png&tbm=isch&source=lnt"
GOOGLE_URL_TEMPLATE = "https://www.google.com/search?q={}+icon+filetype:png&tbm=isch&source=lnt&tbs=iar:s"

IMG_SAVE_PATH = "."#"C:\\Users\\Family\\Documents\\Rainmeter\\Skins\\Dektos by Tibneo\\Dock\\Left\\Icons" # Where are the icons saved?


def get_icon(search_term):
    icon_name = search_term + " icon.png"
    icon_full_path = path.join(IMG_SAVE_PATH, icon_name)

    if icon_name in listdir(IMG_SAVE_PATH):
        return icon_full_path

    print("Looking for " + search_term, "!")
    image = get_image(search_term=search_term)
    image.thumbnail(ICON_SIZE, Image.ANTIALIAS) # make it a thumbnail, in-place

    full_image = make_full_icon(image)
    full_image.save(icon_full_path)

    return icon_full_path


def get_image(search_term):
    parsed_response = BeautifulSoup(get(GOOGLE_URL_TEMPLATE.format(search_term)).text, "html.parser")
    img_element = parsed_response.find("img")

    if img_element is None:
        raise Exception("Could not find image: " + search_term)

    img_response = get(img_element['src'], stream=True)

    return Image.open(BytesIO(img_response.content))


def make_full_icon(image):
    w, h = image.size

    new_image = Image.new("RGBA", (w*3, h))
    img_two = ImageEnhance.Sharpness(image.convert("RGB"))
    img_three = ImageEnhance.Brightness(image.convert("RGB"))

    new_image.paste(make_alpha_icon(image), (0, 0))
    new_image.paste(make_alpha_icon(img_two.enhance(2)), (w, 0))
    new_image.paste(make_alpha_icon(img_three.enhance(1.5)), (w*2, 0))

    return new_image


def make_alpha_icon(image):
    mask = Image.new('L', ICON_SIZE, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + ICON_SIZE, fill=255)

    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    return output
