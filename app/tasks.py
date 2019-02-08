from PIL import Image


def resize_image(filename: str, width: int, height: int) -> None:
    img = Image.open(filename)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(filename)
