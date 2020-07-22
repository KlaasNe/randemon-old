import os

from PIL import Image


class SpriteSheetReader:

    def __init__(self, image, tile_size, margin=0):
        self.sprite_sheet = image
        self.tileSize = tile_size
        self.margin = margin

    def get_tile(self, tile_x, tile_y):
        pos_x = (self.tileSize * tile_x) + (self.margin * (tile_x + 1))
        pos_y = (self.tileSize * tile_y) + (self.margin * (tile_y + 1))
        box = (pos_x, pos_y, pos_x + self.tileSize, pos_y + self.tileSize)
        return self.sprite_sheet.crop(box)


class SpriteSheetWriter:

    def __init__(self, sprite_sheet, tile_size=16):
        self.sprite_sheet = SpriteSheetReader(sprite_sheet, tile_size)
        self.tileSize = tile_size
        self.margin = 1

    def draw_tile(self, sheet_x, sheet_y, draw_sheet, draw_x, draw_y):
        image = self.sprite_sheet.get_tile(sheet_x, sheet_y)
        dest_box = (draw_x, draw_y, draw_x + self.tileSize, draw_y + self.tileSize)
        try:
            draw_sheet.paste(image, dest_box, mask=image)
        except ValueError:
            draw_sheet.paste(image, dest_box)
        except Exception as e:
            print(e)


class DrawSheet:

    def __init__(self, sheet_size_x, sheet_size_y):
        self.sheet_size_x = sheet_size_x
        self.sheet_size_y = sheet_size_y
        self.draw_sheet = Image.new("RGBA", (self.sheet_size_x, self.sheet_size_y), (0, 0, 0, 0))

    def drawable(self):
        return self.draw_sheet

    def show(self):
        self.draw_sheet.show()

    def close(self):
        self.draw_sheet.close()

    def save(self, name):
        self.draw_sheet.save(os.path.join("saved images", name + ".png"), "png")
