import math
from PIL import Image


def image_grayscale_to_dict(image):
    img = Image.open(image).convert('L')  # convert image to 8-bit grayscale
    WIDTH, HEIGHT = img.size

    data = list(img.getdata()) # convert image data to a list of integers
    # convert that to 2D list (list of lists of integers)
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

    # At this point the image's pixels are all in memory and can be accessed
    # individually using data[row][col].

    values = {}
    for position in range(0, WIDTH*HEIGHT):
        x = position % WIDTH
        y = position // WIDTH
        values[(x, y)] = math.ceil(int(data[y][x]) / 16)

    return values

print(min(image_grayscale_to_dict("world_height_map_downscaled2.jpg").values()))
