from io import BytesIO
from os import path, listdir

from PIL import ImageEnhance, Image, ImageOps, ImageDraw
from bs4 import BeautifulSoup
from requests import get

GOOGLE_URL_TEMPLATE = "https://www.google.com/search?q={}+icon+filetype:png&tbm=isch&source=lnt&tbs=isz:ex,iszw:32,iszh:32"

IMG_SAVE_PATH = "."#"C:\\Users\\Family\\Documents\\Rainmeter\\Skins\\Dektos by Tibneo\\Dock\\Left\\Icons" # Where are the icons saved?

def get_icon(search_term):
    assert isinstance(search_term, str)

    icon_name = search_term + " icon.png"

    if icon_name in listdir(IMG_SAVE_PATH):
        return path.join(IMG_SAVE_PATH, icon_name)

    print("Looking for" + search_term, "!")
    parsed = BeautifulSoup(get(GOOGLE_URL_TEMPLATE.format(search_term)).text, "html.parser")
    img = parsed.find("img")

    if img is None:
        raise Exception("Could not find image: " + search_term)

    img_response = get(img['src'], stream=True)

    fullpath = path.join(IMG_SAVE_PATH, icon_name)

    image = Image.open(BytesIO(img_response.content)).convert("RGB")

    full_image = full_icon(image)

    full_image.save(fullpath)

    return fullpath


def full_icon(image):
    w, h = image.size

    new_image = Image.new("RGBA", (w*3, h))
    img_two = ImageEnhance.Sharpness(image.convert("RGB"))
    img_three = ImageEnhance.Brightness(image.convert("RGB"))

    new_image.paste(make_alpha_icon(image), (0, 0))
    new_image.paste(make_alpha_icon(img_two.enhance(2)), (w, 0))
    new_image.paste(make_alpha_icon(img_three.enhance(1.5)), (w*2, 0))

    #new_image.paste(image.convert("RGB").filter(ImageFilter.DETAIL), (w, 0))
    #new_image.paste(image.convert("RGB").filter(ImageFilter.SHARPEN), (w*2, 0))

    return new_image

def make_alpha_icon(image):
    size = (32, 32)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    return output